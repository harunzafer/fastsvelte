import type { ISidebarMenuItem } from '$lib/components/admin-layout/SidebarMenuItem.svelte';
import { APP_MODE } from '$lib/config/constants';

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
		id: 'my_profile',
		icon: 'lucide--user',
		label: 'My Profile',
		url: '/profile/my',
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
				label: 'My Settings',
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

// Filter out org-related menu items when in B2C mode
export const getMenuItems = (): ISidebarMenuItem[] => {
	if (APP_MODE === 'b2c') {
		return adminMenuItems.filter(
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
	return adminMenuItems;
};
