function Sidebar({
  currentPage,
  onNavigate,
  onOpenRequirements,
  onOpenTestCases,
  onOpenAutomation,
  onOpenTestCycles,
  onOpenExecutions,
  onOpenReports
}) {
  return (
    <aside className="sidebar">

      <div className="brand">

        <div className="brand-icon">
          Q
        </div>

        <div>
          <h1>QualiAgent</h1>

          <span>
            AI Quality Engineering
          </span>
        </div>

      </div>


      <nav className="navigation">

        <button
          type="button"
          className={
            currentPage === "dashboard"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={() =>
            onNavigate("dashboard")
          }
        >
          Dashboard
        </button>


        <button
          type="button"
          className={
            currentPage === "projects"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={() =>
            onNavigate("projects")
          }
        >
          Projects
        </button>


        <button
          type="button"
          className={
            currentPage === "requirements"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={
            onOpenRequirements
          }
        >
          Requirements
        </button>


        <button
          type="button"
          className={
            currentPage === "test-cases"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={
            onOpenTestCases
          }
        >
          Test Cases
        </button>


        <button
          type="button"
          className={
            currentPage === "automation"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={
            onOpenAutomation
          }
        >
          Automation
        </button>


        <button
          type="button"
          className={
            currentPage === "test-cycles"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={
            onOpenTestCycles
          }
        >
          Test Cycles
        </button>


        <button
          type="button"
          className={
            currentPage === "executions"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={
            onOpenExecutions
          }
        >
          Executions
        </button>


        <button
          type="button"
          className={
            currentPage === "reports"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={
            onOpenReports
          }
        >
          Reports
        </button>

      </nav>


      <div className="sidebar-footer">

        <span className="status-dot">
        </span>

        QA Workspace

      </div>

    </aside>
  );
}


export default Sidebar;