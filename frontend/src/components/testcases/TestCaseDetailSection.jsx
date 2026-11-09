function TestCaseDetailSection({
  title,
  children
}) {
  return (
    <section className="test-case-detail-section">
      <h4>{title}</h4>
      {children}
    </section>
  );
}


export default TestCaseDetailSection;