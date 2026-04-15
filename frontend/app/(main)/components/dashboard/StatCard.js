export default function StatCard({ label, value }) {
  return (
    <div className="p-4 bg-white rounded-lg shadow text-center" style={{marginBottom:'0.5em'}}>
      <div className="text-gray-500 text-sm">{label} : {value}</div>
    </div>
  );
}