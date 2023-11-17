import axios from 'axios';
import { useState, useEffect } from 'react';
import { useAuth } from './use-auth';
import Cookies from 'universal-cookie';

const axiosInstance = axios.create();

const AxiosInterceptor = ({ children }) => {
    const auth = useAuth();
    const cookies = new Cookies();
    const [token, setToken] = useState(cookies.get('token'));
    
    useEffect(() => {
        if (token) {
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
    }, [token]);
    
    useEffect(() => {
        const interceptor = axiosInstance.interceptors.response.use(
        (response) => response,
        (error) => {
            if (error.response.status === 401) {
            auth.logout();
            }
            return Promise.reject(error);
        }
        );
    
        return () => {
        axiosInstance.interceptors.response.eject(interceptor);
        };
    }, [auth]);
    
    return (
        <AxiosContext.Provider value={{ axiosInstance, setToken }}>
        {children}
        </AxiosContext.Provider>
    );
    }