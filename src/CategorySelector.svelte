<script>
    import Select from 'svelte-select';

	let result = []
	export let category;

	async function doPost () {
		const res = await fetch('http://127.0.0.1:5000/api/categories')
		const json = await res.json()
		result = json.reduce((p, c) => [...c.categories.reduce((pp, cc) => [{name: cc, group: c.group}, ...pp], []), ...p] , [])
	}

	function handleSelect(event) {
        category = event.detail.name;
    }

	doPost();
	const groupBy = (item) => item.group;
	const getOptionLabel = (option) => option.name;
    const getSelectionLabel = (option) => option.name;
</script>

<div>
    <Select items={result} {groupBy} {getOptionLabel} {getSelectionLabel} on:select={handleSelect}></Select>
</div>

<style>
	div {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
</style>