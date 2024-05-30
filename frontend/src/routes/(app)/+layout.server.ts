import type { LayoutServerLoad } from "./$types";
import { PUBLIC_BACKEND_URL } from "$env/static/public";
import axios from 'axios';
import { configRequest } from "$lib/utils";

export const load: LayoutServerLoad = async ({ cookies }) =>  {
    const token = cookies.get('token');

    if (token == undefined) {
        return {'logged': false};
    }

    let url = PUBLIC_BACKEND_URL + "/api/user";
    let auth: RequestAuth = {username: token, password: 'unused'}
    let conf = configRequest('get', url, auth);

    const user: UserInfo = await axios(conf)
        .then((res) => {
            return {
                username: res.data.username, 
                admin: res.data.admin
            };
        })
        .catch((err) => {
            return {
                username: undefined, 
                admin: undefined
            };
        })

    if(user.username === undefined || user.admin === undefined){
        cookies.delete('token', {
            path: '/'
        });
        return {logged: false}; 
    }

    return {'logged': true, user: user}
}