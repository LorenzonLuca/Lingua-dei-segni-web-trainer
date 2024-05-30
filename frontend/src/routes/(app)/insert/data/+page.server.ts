import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_BACKEND_URL } from '$env/static/public';
import { configRequest, getError } from '$lib/utils';
import axios from 'axios';

export const load: PageServerLoad = async ({ cookies }) =>  {
    const token = cookies.get('token');

    if (token == undefined) {
        throw redirect(301, '/');
    }
}

export const actions: Actions = {
    logout: async ({ cookies }) => {
        cookies.delete('token', { path: '/' });
        throw redirect(301, '/')
    },
    insert: async({cookies, request}) =>{
        const formData = await request.formData()
        const data = Object.fromEntries(formData)

        const token = cookies.get('token');

        if (token == undefined) {
            return {'msg': "auth-error"};
        }

        if(!(data.img && data.sign_position && data.base_position && data.words)){
            return {'status': 'NOK', 'msg': 'Mancano dei dati'};
        }

        let img = await fetch(data.img.toString()).then(res => res.blob());

        if(!(data.sign_position && data.base_position && data.words)){
            return {'status': 'NOK', 'msg': 'Inserire tutti i valori richiesti'}
        }

        const bodyFormData = new FormData();
        bodyFormData.append("img", img);
        bodyFormData.append("sign_position", data.sign_position);
        bodyFormData.append("base_position", data.base_position.toString());
        bodyFormData.append("words", data.words.toString());

        let url = PUBLIC_BACKEND_URL + "/api/insert";
        let auth: RequestAuth  = {username: token, password: ""}
        let dataReq = bodyFormData;
        let conf = configRequest('post', url, auth, dataReq);

        let res = await axios(conf).then((res) => {
            return {'status': 'OK', 'msg': 'Gesto inserito con successo'}
        })
        .catch((err) => {
            let m = getError(err.response.data.status,err.response.data.error)
            return {'status': 'NOK', 'msg': m.msg}
        })
        
        return JSON.stringify(res)
    }
}