import { z, type ZodObject, type ZodRawShape } from 'zod';

export function useFormValidation<Shape extends ZodRawShape, T extends ZodObject<Shape>>({
	schema,
	initialValues
}: {
	schema: T;
	initialValues: z.infer<T>;
}) {
	type FormData = z.infer<T>;
	type FormErrors = Partial<Record<keyof FormData, string>>;
	type SchemaKeys = keyof FormData;

	let formData = $state<FormData>({ ...initialValues });
	let errors = $state<FormErrors>({});

	const checkError = (key: SchemaKeys, value: unknown) => {
		const shape = schema.shape as unknown as Record<string, z.ZodType>;
		const fieldSchema = z.object({ [key]: shape[key as string] });
		const result = fieldSchema.safeParse({ [key]: value });

		errors[key] = result.success ? undefined : result.error.issues[0]?.message;
	};

	const handleChange = (e: Event) => {
		const target = e.target as HTMLInputElement | HTMLSelectElement;
		const { name, value, type } = target;
		const key = name as SchemaKeys;

		const parsed: string | number | boolean =
			type === 'checkbox'
				? (target as HTMLInputElement).checked
				: type === 'number' || type === 'range'
					? value === ''
						? ''
						: Number(value)
					: value;

		formData[key] = parsed as any;
		checkError(key, parsed);
	};

	const updateFormData = (key: SchemaKeys, value: unknown) => {
		formData[key] = value as any;
		checkError(key, value);
	};

	const handleSubmit = (e: Event, onSuccess: (data: FormData) => void) => {
		e.preventDefault();
		const result = schema.safeParse(formData);

		if (!result.success) {
			result.error.issues.forEach((issue) => {
				const key = issue.path[0] as SchemaKeys;
				errors[key] = issue.message;
			});
		} else {
			onSuccess(result.data);
		}
	};

	const handleClear = () => {
		formData = { ...initialValues };
		errors = {};
	};

	return {
		formData,
		errors,
		handleChange,
		handleSubmit,
		updateFormData,
		handleClear
	};
}
