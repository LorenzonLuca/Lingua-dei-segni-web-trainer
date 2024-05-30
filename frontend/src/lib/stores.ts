import { readable, writable } from "svelte/store";
import {io} from "./socketConnection";

export const ioStore = readable(io);
export const insertStore = writable<string | undefined>("");
export const wordsStore = writable<Array<Word>>([]);
export const basePosStore = writable(0);
export const deltasStore = writable<Array<WordDelta>>([]);