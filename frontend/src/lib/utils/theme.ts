import type { ITheme } from '$lib/context/ConfigProvider.svelte';

/**
 * Maps user setting theme values to config theme values
 */
export function mapUserThemeToConfig(themeValue: string): ITheme {
	switch (themeValue) {
		case 'light':
			return 'light';
		case 'dark':
			return 'dark';
		case 'auto':
			return 'system';
		default:
			return 'system';
	}
}
