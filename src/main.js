import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		category: '',
		date: new Date(),
	}
});

export default app;
