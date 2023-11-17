import baseURL from "./api_config";
import axios from "axios";

export const createCategory = async (category) => {
    const response = await axios.post(`${baseURL}categories/`, category);
    return response.data;
    }

export const getCategories = async () => {
    const response = await axios.get(`${baseURL}categories/`);
    return response.data;
    }

export const getReccomendations = async () => {
    const response = await axios.get(`${baseURL}recommendations/`);
    return response.data;
    }