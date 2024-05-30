import { type AxiosRequestConfig } from 'axios';
import ita from '$lib/images/languages/ita.png';
import fra from '$lib/images/languages/fra.png';
import * as https from 'https'

export const MAXSIGNS = [7, 23, 31, 17, 12, 20]

export function configRequest(method: string, url: string, auth: RequestAuth, data: any = {}): AxiosRequestConfig{
    let config: AxiosRequestConfig = {
        method: method,
        url: url,
        auth: auth,
        data: data,
        headers: { "Content-Type": "multipart/form-data" },
        httpsAgent: new https.Agent({
            rejectUnauthorized: false
        })
    };
    return config;
}

export function isEmptyString(data: string | undefined): boolean{
    return data == undefined || data === "";
}

export function getSignImage(basePos: number, n: number): string{
    let basename = "https://www.sgb-fss.ch/fileadmin/user_upload/";
    switch(basePos){
        case 0:
            basename += "FAUST_1_";
            break;
        case 1:
            basename += "FLACHHAND_GESCHLOSSEN_2_";
            break;
        case 2:
            basename += "FLACHHAND_OFFEN_3_";
            break;
        case 3:
            basename += "EINZELFINGER_4_";
            break;
        case 4:
            basename += "FLACHHAND_GEKRUMMT_5_";
            break;
        case 5:
            basename += "DAUMENVERBINDEN_6_";
            break;
    }
    basename += String(n).padStart(2, '0');
    basename += ".jpg";
    return basename;
}

export function getLanguageImage(name:string): string{
    switch(name){
        case 'italian':
            return ita;
        case 'french': 
            return fra;
        default:
            return ita;
    }
}

export function calcPerc(d: number): number{
    return 100-((d*100)/4*100);
}

export function getError(statusCode: number = 400, s?:string | undefined): any{
    switch(statusCode){
        case 400:
            switch(s){
                case 'no-hand':
                    return { 'msg': "Nessuna mano trovata all'interno dell'immagine" };
                case 'sign-unrecognized':
                    return { 'msg': "Gesto non riconosciuto, prova con un altra foto" };
                case "username-length-invalid":
                    return { 'msg': 'La lunghezza del nome utente non é valida. Il nome utente deve essere lungo da 4 a 20 caratteri' }
                case "password-invalid":
                    return { 'msg': 'La password non é valida. Una password deve essere lunga almeno 6 caratteri e contenere almeno un numero e un carattere speciale' }
                case "user-exist":
                    return { 'msg': 'Questo nome utente é già utilizzato' }
                case "wrong-format":
                    return {'msg': "Il formato del file non é valido, prova con un'altra immagine"}
                default:
                    return { 'msg': "Qualcosa é andato storto, riprova" };
            }
        case 401:
            return { 'msg': 'Accesso fallito: il nome utente o la password sono sbagliati' }
        default:
            return { 'msg': 'Qualcosa é andato storto, riprova' }
    }
}