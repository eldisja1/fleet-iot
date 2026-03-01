export default function PageTitle({ title }: { title: string }) {
    return (
        <h1 className="text-3xl font-bold text-center mb-10 tracking-wide">
            {title}
        </h1>
    );
}