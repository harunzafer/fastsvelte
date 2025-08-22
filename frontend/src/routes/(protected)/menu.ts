import type { ISidebarMenuItem } from '$lib/components/admin-layout/SidebarMenuItem.svelte';
import { APP_MODE } from '$lib/config/constants';
import type { UserWithRole } from '$lib/api/gen/model/userWithRole';
import { hasRequiredRole } from '$lib/auth/permissions';

export const adminMenuItems: ISidebarMenuItem[] = [
	{
		id: 'notes',
		icon: 'lucide--notebook',
		label: 'Notes',
		url: '/notes',
		minRole: 'readonly'
	},
	{
		id: 'profile',
		icon: 'lucide--user',
		label: 'Profile',
		url: '/profile',
		minRole: 'readonly'
	},
	{
		id: 'billing',
		icon: 'lucide--credit-card',
		label: 'Billing',
		url: '/billing',
		minRole: 'member'
	},
	{
		id: 'org_admin',
		icon: 'lucide--user',
		label: 'Org Admin Tools',
		url: '/org',
		minRole: 'org_admin'
	},

	{
		id: 'org_users',
		icon: 'lucide--user',
		label: 'Org Users',
		url: '/org/users',
		minRole: 'org_admin'
	},
	{
		id: 'settings',
		icon: 'lucide--settings',
		label: 'Settings',
		children: [
			{
				id: 'settings-user',
				label: 'User Preferences',
				url: '/settings/user',
				minRole: 'readonly'
			}
		]
	},
	{
		id: 'organization',
		isTitle: true,
		label: 'Organization',
		minRole: 'org_admin'
	},
	{
		id: 'org-users',
		icon: 'lucide--users',
		label: 'Users',
		children: [
			{
				id: 'org-users-list',
				label: 'All Users',
				url: '/admin/users'
			},
			{
				id: 'org-invitations',
				label: 'Invitations',
				url: '/admin/invitations'
			}
		],
		minRole: 'org_admin'
	},
	{
		id: 'org-settings',
		icon: 'lucide--sliders-horizontal',
		label: 'Org Settings',
		url: '/settings/org',
		minRole: 'org_admin'
	},
	{
		id: 'org-plan',
		icon: 'lucide--badge-dollar-sign',
		label: 'Subscription Plan',
		url: '/admin/plans/current',
		minRole: 'org_admin'
	},
	{
		id: 'system',
		isTitle: true,
		label: 'System',
		minRole: 'sys_admin'
	},
	{
		id: 'system-plans',
		icon: 'lucide--folder-cog',
		label: 'Manage Plans',
		url: '/admin/plans',
		minRole: 'sys_admin'
	}
];

/**
 * Filter menu items based on user role
 */
function filterMenuByRole(
	items: ISidebarMenuItem[],
	user: UserWithRole | null
): ISidebarMenuItem[] {
	return items.filter((item) => {
		// Check if user has required role for this item
		if (!hasRequiredRole(user, item.minRole)) {
			return false;
		}

		// Recursively filter children
		if (item.children) {
			item.children = filterMenuByRole(item.children, user);
			// Only show parent if it has visible children or its own URL
			return item.children.length > 0 || item.url;
		}

		return true;
	});
}

// Filter out org-related menu items when in B2C mode and apply role filtering
export const getMenuItems = (user?: UserWithRole | null): ISidebarMenuItem[] => {
	let items = adminMenuItems;

	// Filter by app mode (B2C vs B2B)
	if (APP_MODE === 'b2c') {
		items = items.filter(
			(item) =>
				![
					'org_admin',
					'org_users',
					'organization',
					'org-users',
					'org-settings',
					'org-plan'
				].includes(item.id)
		);
	}

	// Filter by user role
	if (user) {
		items = filterMenuByRole(items, user);
	}

	return items;
};
