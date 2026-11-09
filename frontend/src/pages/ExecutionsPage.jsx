function ExecutionsPage({
  project,
  executions = [],
  loading,
  onBack,
  onViewExecution
}) {
  if (!project) {
    return (
      <section className="executions-page">

        <div className="empty-state">

          <h4>
            No project selected
          </h4>

          <p>
            Open a project before viewing
            execution history.
          </p>

        </div>

      </section>
    );
  }


  const safeExecutions =
    Array.isArray(executions)
      ? executions
      : [];


  const passedCount =
    safeExecutions.filter(
      (execution) =>
        execution.status === "passed"
    ).length;


  const failedCount =
    safeExecutions.filter(
      (execution) =>
        execution.status === "failed"
    ).length;


  const errorCount =
    safeExecutions.filter(
      (execution) =>
        execution.status === "error"
    ).length;


  const pendingCount =
    safeExecutions.filter(
      (execution) =>
        execution.status === "pending" ||
        execution.status === "running"
    ).length;


  return (
    <section className="executions-page">

      <div className="workspace-header">

        <div>

          <button
            type="button"
            className="back-button"
            onClick={onBack}
          >
            ← Back to Project
          </button>

          <span className="section-label">
            EXECUTION HISTORY
          </span>

          <h3>
            Executions Workspace
          </h3>

          <p>
            Historical Playwright executions
            for {project.name}.
          </p>

          <div className="workspace-tags">

            <span>
              {project.application_type
                ?.toUpperCase() ||
                "UNKNOWN"}
            </span>

            <span>
              {safeExecutions.length}
              {" "}
              Executions
            </span>

          </div>

        </div>

      </div>


      <div className="execution-summary">

        <ExecutionMetric
          label="Total"
          value={
            safeExecutions.length
          }
        />

        <ExecutionMetric
          label="Passed"
          value={
            passedCount
          }
          tone="passed"
        />

        <ExecutionMetric
          label="Failed"
          value={
            failedCount
          }
          tone="failed"
        />

        <ExecutionMetric
          label="Error"
          value={
            errorCount
          }
          tone="error"
        />

        <ExecutionMetric
          label="Pending / Running"
          value={
            pendingCount
          }
          tone="pending"
        />

      </div>


      <div className="executions-content">

        <div className="panel-header">

          <div>

            <span className="section-label">
              HISTORY
            </span>

            <h3>
              Test Executions
            </h3>

          </div>

        </div>


        {loading ? (

          <div className="api-status">
            Loading execution history...
          </div>

        ) : safeExecutions.length === 0 ? (

          <div className="empty-state">

            <h4>
              No executions yet
            </h4>

            <p>
              Run READY automation from the
              Automation Workspace to create
              execution history.
            </p>

          </div>

        ) : (

          <div className="execution-history-list">

            {safeExecutions.map(
              (execution) => (

              <ExecutionCard
                key={execution.id}
                execution={execution}
                onViewExecution={
                  onViewExecution
                }
              />

            ))}

          </div>

        )}

      </div>

    </section>
  );
}


function ExecutionMetric({
  label,
  value,
  tone = ""
}) {
  const className =
    tone
      ? `metric-card execution-metric-${tone}`
      : "metric-card";

  return (
    <article className={className}>

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </article>
  );
}


function ExecutionCard({
  execution,
  onViewExecution
}) {
  const status =
    execution.status ||
    "unknown";

  const duration =
    execution.duration_ms !==
      null &&
    execution.duration_ms !==
      undefined
      ? `${execution.duration_ms} ms`
      : "N/A";

  const exitCode =
    execution.exit_code !==
      null &&
    execution.exit_code !==
      undefined
      ? execution.exit_code
      : "N/A";


  return (
    <article className="execution-history-card">

      <div className="execution-history-main">

        <div className="execution-history-heading">

          <span className="requirement-id">
            Execution #{execution.id}
          </span>

          <span
            className={
              `execution-status execution-${status}`
            }
          >
            {status.toUpperCase()}
          </span>

          <span className="requirement-type">
            {(execution.framework ||
              "unknown")
              .toUpperCase()}
          </span>

        </div>


        <h4>
          {execution.test_case_title ||
            "Untitled test case"}
        </h4>


        <p>
          {execution.test_case_id ||
            "Unknown test case"}

          {" · "}

          {execution.requirement_id ||
            "Unknown requirement"}
        </p>


        <div className="execution-history-meta">

          <span>
            Duration: {duration}
          </span>

          <span>
            Exit Code: {exitCode}
          </span>

          <span>
            {(execution.language ||
              "unknown")
              .toUpperCase()}
          </span>

        </div>

      </div>


      <button
        type="button"
        className="secondary-button"
        onClick={() =>
          onViewExecution(
            execution
          )
        }
      >
        View Details
      </button>

    </article>
  );
}


export default ExecutionsPage;