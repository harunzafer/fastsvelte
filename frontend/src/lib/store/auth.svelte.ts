import type { UserWithRole } from '$lib/api/gen/model/userWithRole';

class AuthStore {
	user = $state<UserWithRole | null>(null);
	isLoading = $state(true);

	get isAuthenticated(): boolean {
		return this.user !== null;
	}

	get userRole(): string | null {
		return this.user?.role?.name || null;
	}

	setLoading(loading: boolean) {
		this.isLoading = loading;
	}

	setUser(user: UserWithRole | null) {
		this.user = user;
		this.isLoading = false;
	}

	clear() {
		this.user = null;
		this.isLoading = false;
	}
}

export const authStore = new AuthStore();
