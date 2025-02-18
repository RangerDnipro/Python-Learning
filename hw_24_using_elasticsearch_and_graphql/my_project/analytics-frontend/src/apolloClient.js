import {ApolloClient, InMemoryCache, HttpLink} from "@apollo/client";

const client = new ApolloClient({
    link: new HttpLink({
        uri: "http://localhost:8000/graphgl/",
        fetchOptions: {
            method: "GET"
        }
    }),
    cache: new InMemoryCache()
})

export default client;
