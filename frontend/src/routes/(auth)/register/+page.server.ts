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
        const confirmPassword = data.get('password2')?.toString();

        if(isEmptyString(username) || isEmptyString(password) || isEmptyString(confirmPassword)){
            return { 'msg': "Riempi tutti i campi"}
        }

        if(password !== confirmPassword){
            return {'msg': "Le due password non corrispondono"}
        }
        
        let url = PUBLIC_BACKEND_URL + "/api/register";
        let auth: RequestAuth  = {username: "", password: ""}
        let dataReq = {'username': username, 'password': password}
        let conf = configRequest('post', url, auth, dataReq);

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
            return getError(res.error.response.status, res.error.response.data.msg);
        }
    }
}