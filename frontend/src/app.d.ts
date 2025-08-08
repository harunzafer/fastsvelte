import type {
	CalendarRangeProps,
	CalendarMonthProps,
	CalendarDateProps,
	CalendarMultiProps
} from 'cally';

// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare module '*.svelte';

declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}
declare module 'svelte-filepond';

declare module 'apexcharts' {
	type ApexGrid = ApexGridType & {
		strokeDashArray?: number | number[];
	};

	type ApexStroke = ApexStrokeType & {
		dashArray: number | number[];
	};

	type ApexForecastDataPoints = ApexForecastDataPointsType & {
		dashArray: number | number[];
	};
}

declare module 'svelte/elements' {
	interface SvelteHTMLElements {
		'calendar-month': CalendarMonthProps & { onchange?: (e: Event) => void } & { class?: string };
		'calendar-range': CalendarRangeProps & { onchange?: (e: Event) => void } & { class?: string };
		'calendar-date': CalendarDateProps & { onchange?: (e: Event) => void } & { class?: string };
		'calendar-multi': CalendarMultiProps & { onchange?: (e: Event) => void } & { class?: string };
	}
}
