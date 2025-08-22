import type { UserWithRole } from '$lib/api/gen/model/userWithRole';

/**
 * Role hierarchy for permission checking
 * NOTE: This must be kept in sync with backend role definitions
 * TODO: Consider fetching this from API endpoint instead of hardcoding
 */
const ROLE_HIERARCHY = {
	readonly: 1,
	member: 2,
	org_admin: 3,
	sys_admin: 4
} as const;

/**
 * Check if user has sufficient role for a required minimum role
 */
export function hasRequiredRole(user: UserWithRole | null, minRole?: string): boolean {
	if (!minRole) return true;
	if (!user?.role) return false;

	const userLevel = ROLE_HIERARCHY[user.role.name as keyof typeof ROLE_HIERARCHY] || 0;
	const requiredLevel = ROLE_HIERARCHY[minRole as keyof typeof ROLE_HIERARCHY] || 0;

	return userLevel >= requiredLevel;
}
