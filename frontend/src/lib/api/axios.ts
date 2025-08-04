// src/lib/api/axios.ts
import axios from 'axios';
import { goto } from '$app/navigation';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const axiosInstance = axios.create({
	baseURL: PUBLIC_API_BASE_URL,
	withCredentials: true
});

axiosInstance.interceptors.response.use(
	(response) => response,
	(error) => {
		if (error.response?.status === 401) {
			goto('/login');
		}
		return Promise.reject(error);
	}
);
