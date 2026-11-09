function Capability({
  title,
  status
}) {
  return (
    <div className="capability">
      <span>{title}</span>
      <small>{status}</small>
    </div>
  );
}


export default Capability;