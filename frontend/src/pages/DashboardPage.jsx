import Capability from "../components/Capability";
import MetricCard from "../components/MetricCard";


function DashboardPage({
  projects,
  requirements,
  testCases,
  latestProject,
  qualitySummary,
  onOpenProject,
  onOpenTestCases,
  onOpenAutomation,
  onOpenExecutions,
  onOpenReports
}) {
  return (
    <>
      <section className="welcome">
        <div>
          <span className="badge">
            QUALIAGENT AI
          </span>

          <h3>
            From requirement to quality confidence.
          </h3>

          <p>
            Analyse requirements, design test cases,
            generate automation and track quality
            from one intelligent QA workspace.
          </p>
        </div>

        <div className="workflow">
          <span>Requirement</span>
          <b>→</b>
          <span>Test Design</span>
          <b>→</b>
          <span>Automation</span>
          <b>→</b>
          <span>Execution</span>
        </div>
      </section>


      <section className="metrics">
        <MetricCard
          label="Projects"
          value={projects.length}
          detail="Active QA workspaces"
        />

        <MetricCard
          label="Requirements"
          value={requirements.length}
          detail="Requirements captured"
        />

        <MetricCard
          label="Test Cases"
          value={testCases.length}
          detail="AI-generated tests"
        />

        <MetricCard
  label="Executions"
  value={
    qualitySummary?.executions ??
    0
  }
  detail={
    qualitySummary?.executions
      ? "Recorded test executions"
      : "No executions yet"
  }
/>
      </section>

      {qualitySummary && (

  <section className="dashboard-quality">

    <div className="panel-header">

      <div>

        <span className="section-label">
          QUALITY STATUS
        </span>

        <h3>
          Current Project Quality
        </h3>

      </div>

    </div>


    <div className="dashboard-quality-grid">

      <MetricCard
        label="Approved Tests"
        value={
          qualitySummary.approved_tests
        }
        detail="Human-approved tests"
      />


      <MetricCard
        label="Automation Ready"
        value={
          qualitySummary.automation_ready
        }
        detail="Generated automation"
      />


      <MetricCard
        label="Passed"
        value={
          qualitySummary.passed
        }
        detail="Successful executions"
      />


      <MetricCard
        label="Failed"
        value={
          qualitySummary.failed
        }
        detail="Failed executions"
      />


      <MetricCard
        label="Pass Rate"
        value={
          `${qualitySummary.pass_rate}%`
        }
        detail="Completed execution pass rate"
      />

    </div>

  </section>

)}

      <section className="dashboard-quick-actions">

  <div className="panel-header">

    <div>

      <span className="section-label">
        QUICK ACTIONS
      </span>

      <h3>
        Continue QA Workflow
      </h3>

    </div>

  </div>


  {!latestProject ? (

    <div className="empty-state">

      <h4>
        No project available
      </h4>

      <p>
        Create a project before opening
        QA workspaces.
      </p>

    </div>

  ) : (

    <div className="dashboard-action-grid">

      <DashboardAction
        title="Test Cases"
        description={
          "Review generated test cases and approval status."
        }
        actionLabel="Open Test Cases"
        onClick={
          onOpenTestCases
        }
      />


      <DashboardAction
        title="Automation"
        description={
          "Generate and review Playwright automation."
        }
        actionLabel="Open Automation"
        onClick={
          onOpenAutomation
        }
      />


      <DashboardAction
        title="Executions"
        description={
          "Review Playwright execution history and evidence."
        }
        actionLabel="Open Executions"
        onClick={
          onOpenExecutions
        }
      />


      <DashboardAction
        title="Reports"
        description={
          "Review project quality, coverage and execution trends."
        }
        actionLabel="Open Reports"
        onClick={
          onOpenReports
        }
      />

    </div>

  )}

</section>


      <section className="content-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="section-label">
                WORKSPACE
              </span>

              <h3>Recent Project</h3>
            </div>

            <button
              type="button"
              className="text-button"
              disabled={!latestProject}
              onClick={() => {
                if (latestProject) {
                  onOpenProject(latestProject);
                }
              }}
            >
              View project
            </button>
          </div>


          <div className="project-card">
            <div className="project-avatar">
              {latestProject
                ? latestProject.name
                    .slice(0, 2)
                    .toUpperCase()
                : "NA"}
            </div>

            <div className="project-details">
              <h4>
                {latestProject
                  ? latestProject.name
                  : "No project available"}
              </h4>

              <p>
                {latestProject
                  ? latestProject.description
                  : "Create your first QA project."}
              </p>

              <div className="project-meta">
                <span>
                  {latestProject
                    ? latestProject.application_type
                        .toUpperCase()
                    : "N/A"}
                </span>

                <span>
                  {requirements.length} Requirements
                </span>

                <span>
                  {testCases.length} Test Cases
                </span>
              </div>
            </div>
          </div>
        </div>


        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="section-label">
                AI WORKFLOW
              </span>

              <h3>QA Capabilities</h3>
            </div>
          </div>

          <div className="capabilities">
            <Capability
              title="Requirement Analysis"
              status="Ready"
            />

            <Capability
              title="Test Case Generation"
              status="Ready"
            />

            <Capability
              title="Web Automation"
              status="Coming next"
            />

            <Capability
              title="API Testing"
              status="Planned"
            />

            <Capability
              title="Mobile Testing"
              status="Planned"
            />
          </div>
        </div>
      </section>
    </>
  );
}

function DashboardAction({
  title,
  description,
  actionLabel,
  onClick
}) {
  return (
    <article className="dashboard-action-card">

      <div>

        <h4>
          {title}
        </h4>

        <p>
          {description}
        </p>

      </div>


      <button
        type="button"
        className="secondary-button"
        onClick={onClick}
      >
        {actionLabel}
      </button>

    </article>
  );
}


export default DashboardPage;