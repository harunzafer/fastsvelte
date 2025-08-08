<script lang="ts">
    import * as FilePond from "filepond";
    import { type FilePondOptions, registerPlugin } from "filepond";
    import FilePondPluginImagePreview from "filepond-plugin-image-preview";
    import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css";
    import "filepond/dist/filepond.css";
    import { onMount } from "svelte";

    registerPlugin(FilePondPluginImagePreview);

    const { credits = false, server, ...others }: FilePondOptions = $props();

    let filepondRef: HTMLInputElement | null = null;

    onMount(() => {
        if (filepondRef) {
            FilePond.create(filepondRef, {
                credits,
                ...others,
                server:
                    typeof server == "string"
                        ? server
                        : {
                              ...server,
                              process: (_, __, ___, load) => load({ message: "done" }),
                          },
            });
        }
    });
</script>

<input type="file" class="filepond" bind:this={filepondRef} />
