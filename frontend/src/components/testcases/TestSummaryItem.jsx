function TestSummaryItem({
  label,
  value
}) {
  return (
    <div className="test-summary-item">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}


export default TestSummaryItem;