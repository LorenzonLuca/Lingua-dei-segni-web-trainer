import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { PUBLIC_BACKEND_URL } from "$env/static/public";
import { configRequest } from "$lib/utils";
import axios from "axios";

export const load: PageServerLoad = async ({ cookies }) =>  {
    const token = cookies.get('token');

    if (token == undefined) {
        throw redirect(301, '/');
    }

    let url = PUBLIC_BACKEND_URL + "/api/history";
    let auth: RequestAuth = {username: token, password: 'unused'}
    let conf = configRequest('get', url, auth);

    const res = await axios(conf)
        .then((res) => {
            return {
                history: res.data.history
            };
        })
        .catch((err) => {
            return {
                history: undefined
            };
        })

    return res
}

export const actions: Actions = {
    logout: async ({ cookies }) => {
        cookies.delete('token', { path: '/' });
        throw redirect(301, '/')
    },
}