// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types
declare namespace App {
	// interface Locals {}
	// interface PageData {}
	// interface Error {}
	// interface Platform {}
}

type RequestAuth = {
	username: string,
	password: string
}

type UserInfo = {
	username: string | undefined,
	admin: number | undefined
}

type Word = {
	word: string,
	category: string,
	language: string,
	basePos?: number,
	signPos?: number
}

type WordDelta = {
	word: Word
	delta: number
}
