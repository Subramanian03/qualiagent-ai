function TestCyclesPage({
  project,
  cycles = [],
  loading = false,
  onCreateCycle,
  onOpenCycle,
  onBack
}) {
  if (!project) {
    return (
      <section className="test-cycles-page">

        <div className="empty-state">

          <h4>
            No project selected
          </h4>

          <p>
            Open a Project before managing
            Test Cycles.
          </p>

        </div>

      </section>
    );
  }


  const safeCycles =
    Array.isArray(cycles)
      ? cycles
      : [];


  return (
    <section className="test-cycles-page">

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
            TEST EXECUTION
          </span>


          <h3>
            Test Cycles
          </h3>


          <p>
            Plan Manual and Automated
            Test Case execution for
            {` ${project.name}`}.
          </p>


          <div className="workspace-tags">

            <span>
              {safeCycles.length}
              {" "}
              CYCLES
            </span>

            <span>
              {(
                project
                  .automation_engine ||
                "playwright"
              ).toUpperCase()}
            </span>

          </div>

        </div>


        <button
          type="button"
          className="primary-button"
          onClick={onCreateCycle}
        >
          Create Test Cycle
        </button>

      </div>


      {loading ? (

        <div className="api-status">
          Loading Test Cycles...
        </div>

      ) : safeCycles.length === 0 ? (

        <div className="empty-state">

          <h4>
            No Test Cycles yet
          </h4>

          <p>
            Create a Cycle and select the
            Manual and Automated Test Cases
            that belong to this testing
            iteration.
          </p>


          <button
            type="button"
            className="primary-button"
            onClick={onCreateCycle}
          >
            Create First Test Cycle
          </button>

        </div>

      ) : (

        <div className="test-cycle-list">

          {safeCycles.map(
            (cycle) => (

              <article
                className="test-cycle-card"
                key={cycle.id}
              >

                <div>

                  <div className="generated-test-heading">

                    <span className="requirement-id">
                      CYCLE #{cycle.id}
                    </span>


                    <span
                      className={
                        `cycle-status cycle-status-${
                          cycle.status ||
                          "draft"
                        }`
                      }
                    >
                      {(
                        cycle.status ||
                        "draft"
                      )
                        .replaceAll(
                          "_",
                          " "
                        )
                        .toUpperCase()}
                    </span>

                  </div>


                  <h4>
                    {cycle.name}
                  </h4>


                  <div className="test-cycle-meta">

                    <span>
                      Release:
                      {" "}
                      {
                        cycle.release ||
                        "Not specified"
                      }
                    </span>

                    <span>
                      Environment:
                      {" "}
                      {
                        cycle.environment ||
                        "Not specified"
                      }
                    </span>

                  </div>

                </div>


                <button
                  type="button"
                  className="secondary-button"
                  onClick={() =>
                    onOpenCycle(
                      cycle
                    )
                  }
                >
                  Open Cycle
                </button>

              </article>

            )
          )}

        </div>

      )}

    </section>
  );
}


export default TestCyclesPage;