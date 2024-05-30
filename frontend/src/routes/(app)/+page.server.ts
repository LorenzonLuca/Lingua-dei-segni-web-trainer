import type { Actions } from './$types';
import { PUBLIC_BACKEND_URL } from '$env/static/public';
import { configRequest, getError } from '$lib/utils';
import axios from 'axios';

export const actions: Actions = {
    logout: async ({ cookies }) => {
        cookies.delete('token', { path: '/' });
    },
    recognize: async({cookies, request}) =>{
        const formData = await request.formData()
        const data = Object.fromEntries(formData)

        let blobImg = await fetch(data.img.toString()).then(res => res.blob());

		const bodyFormData = new FormData();
		bodyFormData.append("img", blobImg);

		let url = PUBLIC_BACKEND_URL + "/api/recognize";
		let auth: RequestAuth = {username: '', password: ''};
		let dataReq = bodyFormData;
		let conf = configRequest('post', url, auth, dataReq);

		let res = await axios(conf).then((res) => {
			return res.data;
		})
        .catch((err) => {
            let m = getError(err.response.data.status,err.response.data.error)
            return {'status': 'NOK', 'msg': m.msg}
        })

        let json_res = JSON.stringify(res);

        return json_res;
    }
}