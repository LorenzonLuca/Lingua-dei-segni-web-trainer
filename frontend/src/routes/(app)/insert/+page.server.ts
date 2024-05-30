import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

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
    }
}