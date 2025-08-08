<script lang="ts">
    type ILogo = {
        className?: string;
    };

    let { className }: ILogo = $props();
</script>

<img src="/images/logo/logo-dark.png" alt="logo-dark" class={`hidden h-5 dark:block ${className ?? ""}`} />
<img src="/images/logo/logo-light.png" alt="logo-light" class={`h-5 dark:hidden block ${className ?? ""}`} />
