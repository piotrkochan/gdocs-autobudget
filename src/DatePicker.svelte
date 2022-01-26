<script>
  import { DateInput, DatePicker, localeFromDateFnsLocale } from 'date-picker-svelte'
  import { pl } from 'date-fns/locale'
  export let date;
  let locale = localeFromDateFnsLocale(pl)
  let format = 'dd.MM.yyyy'
</script>

<DateInput bind:value={date} {locale} {format} />
<!--<DatePicker bind:value={date} {locale} />-->