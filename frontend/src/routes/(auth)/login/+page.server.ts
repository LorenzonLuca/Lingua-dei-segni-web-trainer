import type { Actions } from './$types';
import { configRequest, getError, isEmptyString }  from "$lib/utils";
import { PUBLIC_BACKEND_URL } from '$env/static/public';
import axios from 'axios';
import { redirect } from '@sveltejs/kit';

export const actions: Actions = {
    default: async ({ cookies, request }) => {
        const data = await request.formData();
        const username = data.get('username')?.toString();
        const password = data.get('password')?.toString();

        if(isEmptyString(username) || isEmptyString(password)){
            return { 'msg': "Riempi tutti i campi"}
        }
        
        let url = PUBLIC_BACKEND_URL + "/api/login";
        let auth: RequestAuth = {username: username!, password: password!}
        let conf = configRequest('get', url, auth);

        const res = await axios(conf)
            .then((res) => {
                cookies.set('token', res.data.token, {
                    path: '/',
                    maxAge: 60 * 60 * 24 * 30
                })
                return { 'status': true, 'error': undefined };
            })
            .catch((err) => {
                return { 'status': false, 'error': err };
            })

        if (res.status) {
            throw redirect(302, '/');
        } else {
            return getError(res.error.response.status);
        }
    }
}