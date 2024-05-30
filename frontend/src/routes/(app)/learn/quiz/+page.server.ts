import { redirect, type Actions } from "@sveltejs/kit";
import { PUBLIC_BACKEND_URL } from "$env/static/public";
import { configRequest } from "$lib/utils";
import axios from "axios";

export const actions: Actions = {
    logout: async ({ cookies }) => {
        cookies.delete('token', { path: '/' });
        throw redirect(301, '/')
    },
    save: async ({cookies, request}) => {
        const formData = await request.formData()
        const data = Object.fromEntries(formData)

        const token = cookies.get('token');

        if (token == undefined) {
            return;
        }

        const bodyFormData = new FormData();
        bodyFormData.append("word", data.word);
        bodyFormData.append("value", data.value);

        let url = PUBLIC_BACKEND_URL + "/api/history/add";
        let auth: RequestAuth  = {username: token, password: ""}
        let dataReq = bodyFormData;
        let conf = configRequest('post', url, auth, dataReq);

        await axios(conf)
    }
}