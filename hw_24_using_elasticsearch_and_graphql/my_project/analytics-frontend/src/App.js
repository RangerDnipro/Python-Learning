import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

import React, { useState, useEffect } from 'react';
import { gql, useQuery } from '@apollo/client';
import { Bar, Pie } from 'react-chartjs-2';

// GraphQL-запит для підрахунку документів за категоріями
const DOCUMENT_COUNT_BY_CATEGORY = gql`
  query {
    documentCountByCategory
  }
`;

// GraphQL-запит для пошуку документів
const SEARCH_DOCUMENTS = gql`
  query SearchDocuments($search: String!) {
    searchDocuments(search: $search) {
      title
      description
      createdAt
    }
  }
`;

// Запити для кругової діаграми
const DOCUMENTS_BY_AUTHORS = gql`
  query {
    documentsByAuthors {
      name
      count
    }
  }
`;

const DOCUMENTS_BY_CATEGORIES = gql`
  query {
    documentsByCategories {
      name
      count
    }
  }
`;

const DOCUMENTS_BY_TAGS = gql`
  query {
    documentsByTags {
      name
      count
    }
  }
`;

function App() {
  const { data: categoryData, loading: categoryLoading } = useQuery(DOCUMENT_COUNT_BY_CATEGORY);
  const [search, setSearch] = useState('');
  const [chartData, setChartData] = useState({ labels: [], datasets: [] });

  const { data: searchData, refetch } = useQuery(SEARCH_DOCUMENTS, {
    variables: { search: '' },
    skip: true,
  });

  const [groupingType, setGroupingType] = useState('authors'); // Тип групування для кругової діаграми
  const { data: authorsData } = useQuery(DOCUMENTS_BY_AUTHORS);
  const { data: categoriesData } = useQuery(DOCUMENTS_BY_CATEGORIES);
  const { data: tagsData } = useQuery(DOCUMENTS_BY_TAGS);

  useEffect(() => {
    if (categoryData?.documentCountByCategory) {
      updateChartWithCategories(categoryData.documentCountByCategory);
    }
  }, [categoryData]);

  const handleSearch = () => {
    refetch({ search }).then((response) => {
      if (response.data?.searchDocuments?.length > 0) {
        updateChartWithSearchResults(response.data.searchDocuments);
      }
    });
  };

  const updateChartWithCategories = (data) => {
    const labels = data.map((item) => item.split(':')[0]);
    const values = data.map((item) => parseInt(item.split(':')[1]));

    setChartData({
      labels,
      datasets: [
        {
          label: 'Document Count by Category',
          data: values,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
      ],
    });
  };

  const updateChartWithSearchResults = (documents) => {
    const labels = documents.map((doc) => doc.title);
    const values = labels.map(() => 1);

    setChartData({
      labels,
      datasets: [
        {
          label: 'Search Results',
          data: values,
          backgroundColor: 'rgba(153, 102, 255, 0.6)',
        },
      ],
    });
  };

  const getPieChartData = () => {
    let labels = [];
    let counts = [];

    if (groupingType === 'authors' && authorsData) {
      labels = authorsData.documentsByAuthors.map((item) => item.name);
      counts = authorsData.documentsByAuthors.map((item) => item.count);
    } else if (groupingType === 'categories' && categoriesData) {
      labels = categoriesData.documentsByCategories.map((item) => item.name);
      counts = categoriesData.documentsByCategories.map((item) => item.count);
    } else if (groupingType === 'tags' && tagsData) {
      labels = tagsData.documentsByTags.map((item) => item.name);
      counts = tagsData.documentsByTags.map((item) => item.count);
    }

    return {
      labels,
      datasets: [
        {
          label: 'Count',
          data: counts,
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        },
      ],
    };
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Document Analytics Dashboard</h1>

      {/* Графік за категоріями */}
      {categoryLoading ? (
        <p>Loading categories...</p>
      ) : (
        <Bar data={chartData} options={{ responsive: true }} />
      )}

      {/* Пошук */}
      <div style={{ marginTop: '2rem' }}>
        <h2>Search Documents</h2>
        <input
          type="text"
          placeholder="Enter keywords"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Кругова діаграма */}
      <div style={{ marginTop: '2rem' }}>
        <h2>Grouping by {groupingType.charAt(0).toUpperCase() + groupingType.slice(1)}</h2>
        <select value={groupingType} onChange={(e) => setGroupingType(e.target.value)}>
          <option value="authors">Authors</option>
          <option value="categories">Categories</option>
          <option value="tags">Tags</option>
        </select>
        <Pie data={getPieChartData()} options={{ responsive: true }} />
      </div>
    </div>
  );
}

export default App;
