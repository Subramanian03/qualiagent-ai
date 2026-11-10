import {
  useEffect,
  useState
} from "react";

function ReportsPage({
  project,
  summary,
  cycleSummary,
  traceability,
  filters,
  filterOptions,
  filtersLoading = false,
  onApplyFilters,
  onResetFilters,
  coverage = [],
  executions = [],
  loading,
  onViewExecution,
  releaseQuality,
  releasePdfDownloading = false,
  onDownloadReleasePdf,
  onBack
}) {
  const [
  draftFilters,
  setDraftFilters
] = useState({
  release: "",
  environment: "",
  cycle_status: "",
  result_status: "",
  execution_mode: ""
});


useEffect(
  () => {

    setDraftFilters({
      release:
        filters?.release ||
        "",

      environment:
        filters?.environment ||
        "",

      cycle_status:
        filters?.cycle_status ||
        "",

      result_status:
        filters?.result_status ||
        "",

      execution_mode:
        filters?.execution_mode ||
        ""
    });

  },
  [filters]
);

  if (!project) {
    return (
      <section className="reports-page">

        <div className="empty-state">

          <h4>
            No project selected
          </h4>

          <p>
            Open a project before viewing
            quality reports.
          </p>

        </div>

      </section>
    );
  }

  const safeExecutions =
  Array.isArray(
    executions
  )
    ? executions
    : [];


  const safeCoverage =
  Array.isArray(
    coverage
  )
    ? coverage
    : [];


   const safeRequirements =
  Array.isArray(
    traceability?.requirements
  )
    ? traceability.requirements
    : [];

  const releaseRisks =
  Array.isArray(
    releaseQuality?.risks
  )
    ? releaseQuality.risks
    : [];


  const recentExecutions =
  safeExecutions.slice(
    0,
    10
  );

  const releases =
  Array.isArray(
    filterOptions?.releases
  )
    ? filterOptions.releases
    : [];


const environments =
  Array.isArray(
    filterOptions?.environments
  )
    ? filterOptions.environments
    : [];


const cycleStatuses =
  Array.isArray(
    filterOptions?.cycle_statuses
  )
    ? filterOptions.cycle_statuses
    : [];


const resultStatuses =
  Array.isArray(
    filterOptions?.result_statuses
  )
    ? filterOptions.result_statuses
    : [];


const executionModes =
  Array.isArray(
    filterOptions?.execution_modes
  )
    ? filterOptions.execution_modes
    : [];

  function handleFilterChange(
  event
) {
  const {
    name,
    value
  } = event.target;


  setDraftFilters(
    (current) => ({
      ...current,
     [name] : value
    })
  );
}


function handleFilterSubmit(
  event
) {
  event.preventDefault();


  if (
    filtersLoading ||
    !onApplyFilters
  ) {
    return;
  }


  onApplyFilters({
    ...draftFilters
  });
}


function handleFilterReset() {
  const emptyFilters = {
    release: "",
    environment: "",
    cycle_status: "",
    result_status: "",
    execution_mode: ""
  };


  setDraftFilters(
    emptyFilters
  );


  if (onResetFilters) {

    onResetFilters();
  }
}

function handleFilterReset() {
  const emptyFilters = {
    release: "",
    environment: "",
    cycle_status: "",
    result_status: "",
    execution_mode: ""
  };


  setDraftFilters(
    emptyFilters
  );


  if (onResetFilters) {

    onResetFilters();
  }
}

  return (
    <section className="reports-page">

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
            QUALITY REPORTING
          </span>

          <h3>
            Project Quality Report
          </h3>

          <p>
            Quality summary for{" "}
            {project.name}.
          </p>

          <div className="workspace-tags">

            <span>
              {project.application_type
                ?.toUpperCase() ||
                "UNKNOWN"}
            </span>

            <span>
              LIVE PROJECT DATA
            </span>

          </div>

        </div>

      </div>

      <section className="report-filter-panel">

  <div className="panel-header">

    <div>

      <span className="section-label">
        REPORT FILTERS
      </span>

      <h3>
        Release and Execution Drill-down
      </h3>

    </div>

  </div>


  <form
    className="report-filter-form"
    onSubmit={
      handleFilterSubmit
    }
  >

    <div className="form-field">

      <label htmlFor="report-release">
        Release
      </label>

      <select
        id="report-release"
        name="release"
        value={
          draftFilters.release
        }
        disabled={
  filtersLoading
}
        onChange={
          handleFilterChange
        }
      >

        <option value="">
          All Releases
        </option>

        {releases.map(
            (release) => (

            <option
              key={release}
              value={release}
            >
              {release}
            </option>

          )
        )}

      </select>

    </div>


    <div className="form-field">

      <label htmlFor="report-environment">
        Environment
      </label>

      <select
        id="report-environment"
        name="environment"
        value={
          draftFilters.environment
        }
        disabled={
          filtersLoading
        }
        onChange={
          handleFilterChange
        }
      >

        <option value="">
          All Environments
        </option>

        {environments.map(
            (environment) => (

            <option
              key={environment}
              value={environment}
            >
              {environment}
            </option>

          )
        )}

      </select>

    </div>


    <div className="form-field">

      <label htmlFor="report-cycle-status">
        Cycle Status
      </label>

      <select
        id="report-cycle-status"
        name="cycle_status"
        value={
          draftFilters.cycle_status
        }
        disabled={
          filtersLoading
        }
        onChange={
          handleFilterChange
        }
      >

        <option value="">
          All Cycle Statuses
        </option>

        {cycleStatuses.map(
            (status) => (

            <option
              key={status}
              value={status}
            >
              {status
                .replaceAll(
                  "_",
                  " "
                )
                .toUpperCase()}
            </option>

          )
        )}

      </select>

    </div>


    <div className="form-field">

      <label htmlFor="report-result-status">
        Result
      </label>

      <select
        id="report-result-status"
        name="result_status"
        value={
          draftFilters.result_status
        }
        disabled={
          filtersLoading
        }
        onChange={
          handleFilterChange
        }
      >

        <option value="">
          All Results
        </option>

        {resultStatuses.map(
            (status) => (

            <option
              key={status}
              value={status}
            >
              {status
                .replaceAll(
                  "_",
                  " "
                )
                .toUpperCase()}
            </option>

          )
        )}

      </select>

    </div>


    <div className="form-field">

      <label htmlFor="report-execution-mode">
        Execution Mode
      </label>

      <select
        id="report-execution-mode"
        name="execution_mode"
        value={
          draftFilters.execution_mode
        }
        disabled={
          filtersLoading
        }
        onChange={
          handleFilterChange
        }
      >

        <option value="">
          All Modes
        </option>

        {executionModes.map(
            (mode) => (

            <option
              key={mode}
              value={mode}
            >
              {mode.toUpperCase()}
            </option>

          )
        )}

      </select>

    </div>


    <div className="report-filter-actions">

  <button
    type="button"
    className="secondary-button"
    disabled={
      filtersLoading ||
      !onResetFilters
    }
    onClick={
      handleFilterReset
    }
  >
    Reset
  </button>


  <button
    type="submit"
    className="primary-button"
    disabled={
      filtersLoading
    }
  >
    {filtersLoading
      ? "Applying..."
      : "Apply Filters"}
  </button>

</div>

  </form>

</section>

      {filters?.release && (

  <section
    className={
      `release-readiness-panel release-readiness-${
        releaseQuality?.signal ||
        "unknown"
      }`
    }
  >

    <div className="release-readiness-heading">

  <div>

    <span className="section-label">
      RELEASE READINESS
    </span>

    <h3>
      {filters.release}

      {filters.environment
        ? ` · ${filters.environment}`
        : ""}
    </h3>

  </div>


  <div className="release-readiness-actions">

    <span
      className={
        `release-readiness-signal release-readiness-signal-${
          releaseQuality?.signal ||
          "unknown"
        }`
      }
    >
      {releaseQuality?.signal
        ? releaseQuality.signal
            .replaceAll(
              "_",
              " "
            )
            .toUpperCase()
        : "UNAVAILABLE"}
    </span>


    <button
      type="button"
      className="secondary-button"
      disabled={
        releasePdfDownloading ||
        !releaseQuality ||
        !onDownloadReleasePdf
      }
      onClick={
        onDownloadReleasePdf
      }
    >
      {releasePdfDownloading
        ? "Downloading..."
        : "Download PDF"}
    </button>

  </div>

</div>


    {!releaseQuality ? (

      <div className="empty-state">

        <p>
          Release Quality could not be
          calculated.
        </p>

      </div>

    ) : (

      <>

        <div className="report-metric-grid">

          <ReportMetric
            label="Test Cycles"
            value={
              releaseQuality
                .execution
                .cycles
            }
          />


          <ReportMetric
            label="Planned Tests"
            value={
              releaseQuality
                .execution
                .planned_tests
            }
          />


          <ReportMetric
            label="Completed"
            value={
              releaseQuality
                .execution
                .completed_tests
            }
          />


          <ReportMetric
            label="Passed"
            value={
              releaseQuality
                .execution
                .passed
            }
            tone="success"
          />


          <ReportMetric
            label="Failed"
            value={
              releaseQuality
                .execution
                .failed
            }
            tone="danger"
          />


          <ReportMetric
            label="Blocked"
            value={
              releaseQuality
                .execution
                .blocked
            }
            tone="warning"
          />


          <ReportMetric
            label="Not Run"
            value={
              releaseQuality
                .execution
                .not_run
            }
            tone="neutral"
          />


          <ReportMetric
            label="Errors"
            value={
              releaseQuality
                .execution
                .error
            }
            tone="warning"
          />


          <ReportMetric
            label="Pass Rate"
            value={
              `${
                releaseQuality
                  .execution
                  .pass_rate
              }%`
            }
            tone={
              getPassRateTone(
                releaseQuality
                  .execution
                  .pass_rate
              )
            }
            featured
          />

        </div>


        <div className="release-readiness-reasons">

          {(
            Array.isArray(
              releaseQuality.reasons
            )
              ? releaseQuality.reasons
              : []
          ).map(
            (reason) => (

              <div
                className="release-readiness-reason"
                key={reason.code}
              >

                <strong>
                  {reason.code
                    .replaceAll(
                      "_",
                      " "
                    )
                    .toUpperCase()}
                </strong>

                <p>
                  {reason.message}
                </p>

              </div>

            )
          )}

        </div>

        <div className="release-risk-section">

  <div className="release-risk-section-heading">

    <div>

      <span className="section-label">
        RELEASE RISKS
      </span>

      <h4>
        Tests requiring attention
      </h4>

    </div>


    <span className="release-risk-count">
      {releaseRisks.length}
    </span>

  </div>


  {releaseRisks.length === 0 ? (

    <div className="release-risk-empty">

      No Test Case risks were identified
      for this Release and Environment.

    </div>

  ) : (

    <div className="release-risk-list">

      {releaseRisks.map(
        (risk) => (

          <ReleaseRiskCard
            key={
              `${
                risk.cycle_id
              }-${
                risk.test_case_db_id
              }-${
                risk.risk_code
              }`
            }

            risk={
              risk
            }

            executions={
              safeExecutions
            }

            onViewExecution={
              onViewExecution
            }
          />

        )
      )}

    </div>

  )}

</div>

      </>

    )}

  </section>

)}


      {loading ? (

        <div className="api-status">
          Loading project quality report...
        </div>

      ) : !summary ? (

        <div className="empty-state">

          <h4>
            Report unavailable
          </h4>

          <p>
            Quality summary could not be
            loaded for this project.
          </p>

        </div>

      ) : (

        <>

          <ReportSection
            label="PROJECT QUALITY"
            title="Test Design"
          >

            <div className="report-metric-grid">

              <ReportMetric
                label="Requirements"
                value={
                  summary.requirements
                }
              />

              <ReportMetric
                label="Test Cases"
                value={
                  summary.test_cases
                }
              />

              <ReportMetric
                label="Draft"
                value={
                  summary.draft_tests
                }
                tone="neutral"
              />

              <ReportMetric
                label="Approved"
                value={
                  summary.approved_tests
                }
                tone="success"
              />

              <ReportMetric
                label="Rejected"
                value={
                  summary.rejected_tests
                }
                tone="danger"
              />

            </div>

          </ReportSection>


          <ReportSection
            label="AUTOMATION"
            title="Automation Readiness"
          >

            <div className="report-metric-grid report-metric-grid-small">

              <ReportMetric
                label="Candidates"
                value={
                  summary
                    .automation_candidates
                }
              />

              <ReportMetric
                label="Ready"
                value={
                  summary
                    .automation_ready
                }
                tone="success"
              />

            </div>

          </ReportSection>

          {cycleSummary ? (

  <ReportSection
    label="CYCLE EXECUTION"
    title="Cycle Quality"
  >

    <div className="report-metric-grid">

      <ReportMetric
        label="Test Cycles"
        value={
          cycleSummary.cycles.total
        }
      />


      <ReportMetric
        label="Completed Cycles"
        value={
          cycleSummary.cycles.completed
        }
        tone="success"
      />


      <ReportMetric
        label="In Progress"
        value={
          cycleSummary.cycles.in_progress
        }
        tone="warning"
      />


      <ReportMetric
        label="Completed Tests"
        value={
          cycleSummary.results.completed
        }
      />


      <ReportMetric
        label="Passed"
        value={
          cycleSummary.results.passed
        }
        tone="success"
      />


      <ReportMetric
        label="Failed"
        value={
          cycleSummary.results.failed
        }
        tone="danger"
      />


      <ReportMetric
        label="Blocked"
        value={
          cycleSummary.results.blocked
        }
        tone="warning"
      />


      <ReportMetric
        label="Not Run"
        value={
          cycleSummary.results.not_run
        }
        tone="neutral"
      />


      <ReportMetric
        label="Pass Rate"
        value={
          `${cycleSummary.results.pass_rate}%`
        }
        tone={
          getPassRateTone(
            cycleSummary.results.pass_rate
          )
        }
        featured
      />

    </div>

  </ReportSection>

) : (

  <ReportSection
    label="CYCLE EXECUTION"
    title="Cycle Quality"
  >

    <div className="empty-state">

      <h4>
        Cycle reporting unavailable
      </h4>

      <p>
        Cycle execution metrics could not
        be loaded for this Project.
      </p>

    </div>

  </ReportSection>

)}

         {cycleSummary && (

  <ReportSection
    label="EXECUTION MODES"
    title="Manual vs Automation"
  >

    <div className="cycle-report-split">

      <div className="cycle-report-mode">

        <div className="cycle-report-mode-header">

          <span>
            MANUAL
          </span>

          <strong>
            {cycleSummary.manual.total}
          </strong>

        </div>


        <div className="report-metric-grid report-metric-grid-small">

          <ReportMetric
            label="Passed"
            value={
              cycleSummary.manual.passed
            }
            tone="success"
          />

          <ReportMetric
            label="Failed"
            value={
              cycleSummary.manual.failed
            }
            tone="danger"
          />

          <ReportMetric
            label="Blocked"
            value={
              cycleSummary.manual.blocked
            }
            tone="warning"
          />

          <ReportMetric
            label="Skipped"
            value={
              cycleSummary.manual.skipped
            }
            tone="neutral"
          />

        </div>

      </div>


      <div className="cycle-report-mode">

        <div className="cycle-report-mode-header">

          <span>
            AUTOMATION
          </span>

          <strong>
            {cycleSummary.automation.total}
          </strong>

        </div>


        <div className="report-metric-grid report-metric-grid-small">

          <ReportMetric
            label="Passed"
            value={
              cycleSummary.automation.passed
            }
            tone="success"
          />

          <ReportMetric
            label="Failed"
            value={
              cycleSummary.automation.failed
            }
            tone="danger"
          />

          <ReportMetric
            label="Errors"
            value={
              cycleSummary.automation.error
            }
            tone="warning"
          />

        </div>

      </div>

    </div>

  </ReportSection>

)}

        {cycleSummary && (

  <ReportSection
    label="TEST EVIDENCE"
    title="Cycle Execution Evidence"
  >


    <div className="report-metric-grid report-metric-grid-small">

      <ReportMetric
        label="Executions"
        value={
          cycleSummary.evidence.executions
        }
      />


      <ReportMetric
        label="Screenshots"
        value={
          cycleSummary.evidence.screenshots
        }
      />


      <ReportMetric
        label="Traces"
        value={
          cycleSummary.evidence.traces
        }
      />

    </div>

  </ReportSection>

  

)}

          <ReportSection
  label="TRACEABILITY"
  title="Requirement to Execution"
>

  {safeRequirements.length === 0 ? (

    <div className="empty-state">

      <h4>
        No traceability data
      </h4>

      <p>
        No Requirements are available for
        Cycle traceability in this Project.
      </p>

    </div>

  ) : (

    <div className="cycle-traceability-tree">

      {safeRequirements.map(
        (requirement) => (

          <section
            className="traceability-requirement"
            key={requirement.id}
          >

            <div className="traceability-requirement-header">

              <span className="requirement-id">
                {requirement.requirement_id}
              </span>

              <strong>
                {requirement.title}
              </strong>

            </div>


            <div className="traceability-scenario-list">

              {(
  Array.isArray(
    requirement.scenarios
  )
    ? requirement.scenarios
    : []
).map(
                  (scenario) => (

                  <section
                    className="traceability-scenario"
                    key={scenario.id}
                  >

                    <div className="traceability-scenario-header">

                      <span>
                        {scenario.scenario_id}
                      </span>

                      <strong>
                        {scenario.title}
                      </strong>

                    </div>


                    <div className="traceability-test-list">

                      {(
  Array.isArray(
    scenario.test_cases
  )
    ? scenario.test_cases
    : []
).map(
                          (testCase) => (

                          <TraceabilityTestCase
  key={
    testCase.id
  }

  testCase={
    testCase
  }

  executions={
    safeExecutions
  }

  onViewExecution={
    onViewExecution
  }
/>

                        )
                      )}

                    </div>

                  </section>

                )
              )}

            </div>

          </section>

        )
      )}

    </div>

  )}

</ReportSection>

          <ReportSection
  label="LEGACY EXECUTION"
  title="Standalone Automation Execution"
>

            <div className="report-metric-grid">

              <ReportMetric
                label="Executions"
                value={
                  summary.executions
                }
              />

              <ReportMetric
                label="Passed"
                value={
                  summary.passed
                }
                tone="success"
              />

              <ReportMetric
                label="Failed"
                value={
                  summary.failed
                }
                tone="danger"
              />

              <ReportMetric
                label="Errors"
                value={
                  summary.errors
                }
                tone="warning"
              />

              <ReportMetric
                label="Pass Rate"
                value={
                  `${summary.pass_rate}%`
                }
                tone={
                  getPassRateTone(
                    summary.pass_rate
                  )
                }
                featured
              />

            </div>

          </ReportSection>


          <section className="quality-overview">

            <div>

              <span className="section-label">
                QUALITY SIGNAL
              </span>

              <h3>
                Current Project Position
              </h3>

            </div>


            <QualitySignal
              summary={summary}
            />

          </section>

          <ReportSection
  label="REQUIREMENT COVERAGE"
  title="Coverage by Requirement"
>

  {safeCoverage.length === 0 ? (

    <div className="empty-state">

      <h4>
        No requirement coverage yet
      </h4>

      <p>
        Add requirements and generate test
        cases to establish coverage.
      </p>

    </div>

  ) : (

    <div className="requirement-coverage-list">

      {safeCoverage.map(
        (item) => (

        <article
          className="requirement-coverage-card"
          key={
            item.requirement_db_id
          }
        >

          <div className="requirement-coverage-heading">

            <div>

              <span className="requirement-id">
                {item.requirement_id}
              </span>

              <h4>
                {item.title}
              </h4>

            </div>


            <CoverageStatus
              status={
                item.latest_status
              }
            />

          </div>


          <div className="requirement-coverage-metrics">

            <CoverageMetric
              label="Tests"
              value={
                item.test_cases
              }
            />

            <CoverageMetric
              label="Approved"
              value={
                item.approved_tests
              }
            />

            <CoverageMetric
              label="Automation Ready"
              value={
                item.automation_ready
              }
            />

            <CoverageMetric
              label="Executions"
              value={
                item.executions
              }
            />

          </div>

        </article>

      ))}

    </div>

  )}

</ReportSection>

          <ReportSection
  label="EXECUTION TREND"
  title="Recent Test Results"
>

  {recentExecutions.length === 0 ? (

    <div className="empty-state">

      <h4>
        No execution history yet
      </h4>

      <p>
        Run READY automation to establish
        an execution trend.
      </p>

    </div>

  ) : (

    <div className="execution-trend-list">

      {recentExecutions.map(
        (execution) => (

        <ExecutionTrendItem
          key={execution.id}
          execution={execution}
        />

      ))}

    </div>

  )}

</ReportSection>

        </>

      )}

    </section>
  );
}


function ReportSection({
  label,
  title,
  children
}) {
  return (
    <section className="report-section">

      <div className="panel-header">

        <div>

          <span className="section-label">
            {label}
          </span>

          <h3>
            {title}
          </h3>

        </div>

      </div>

      {children}

    </section>
  );
}

function ReleaseRiskCard({
  risk,
  executions,
  onViewExecution
}) {
  const severity = String(
    risk.severity ||
    "high"
  ).toLowerCase();


  const resultStatus = String(
    risk.result_status ||
    "unknown"
  ).toLowerCase();


  const execution =
    risk.execution;


  const safeExecutionList =
    Array.isArray(
      executions
    )
      ? executions
      : [];


  const fullExecution =
    execution
      ? safeExecutionList.find(
          (item) =>
            item.id ===
            execution.id
        )
      : null;


  return (
    <article
      className={
        `release-risk-card release-risk-${severity}`
      }
    >

      <div className="release-risk-card-heading">

        <div>

          <div className="release-risk-badges">

            <span
              className={
                `release-risk-severity release-risk-severity-${severity}`
              }
            >
              {severity.toUpperCase()}
            </span>


            <span
              className={
                `cycle-item-status cycle-item-status-${resultStatus}`
              }
            >
              {resultStatus
                .replaceAll(
                  "_",
                  " "
                )
                .toUpperCase()}
            </span>

          </div>


          <span className="requirement-id">
            {risk.test_case_id}
          </span>


          <h4>
            {risk.test_case_title}
          </h4>

        </div>


        <span className="release-risk-code">
          {String(
            risk.risk_code ||
            "RISK"
          )
            .replaceAll(
              "_",
              " "
            )
            .toUpperCase()}
        </span>

      </div>


      <div className="release-risk-traceability">

        <span>
          Requirement:
          {" "}
          {risk.requirement_id}
        </span>


        <span>
          Scenario:
          {" "}
          {risk.scenario_id}
        </span>


        <span>
          Cycle:
          {" "}
          {risk.cycle_name}
          {" "}
          (#{risk.cycle_id})
        </span>


        <span>
          {String(
            risk.execution_mode ||
            "unknown"
          ).toUpperCase()}
        </span>


        {risk.environment && (

          <span>
            Environment:
            {" "}
            {risk.environment}
          </span>

        )}

      </div>


      {risk.automation_version_id !=
        null && (

        <div className="release-risk-automation">

          <span>
            Frozen Automation:
          </span>

          <strong>

            {risk.automation_engine
              ? String(
                  risk.automation_engine
                ).toUpperCase()
              : "AUTOMATION"}

            {risk.automation_version_number !=
              null && (
              <>
                {" "}
                V
                {risk
                  .automation_version_number}
              </>
            )}

          </strong>

        </div>

      )}


      {execution && (

        <div className="release-risk-execution">

          <span>
            Execution #{execution.id}
          </span>


          <span>
            Exit Code:
            {" "}
            {execution.exit_code ??
              "N/A"}
          </span>


          <span>
            Duration:
            {" "}
            {execution.duration_ms !=
              null
              ? formatDuration(
                  execution.duration_ms
                )
              : "N/A"}
          </span>


          {execution.screenshot_available && (

            <span className="traceability-evidence-available">
              SCREENSHOT
            </span>

          )}


          {execution.trace_available && (

            <span className="traceability-evidence-available">
              TRACE
            </span>

          )}

        </div>

      )}


      {execution && (

        <div className="release-risk-actions">

          <button
            type="button"
            className="secondary-button"
            disabled={
              !fullExecution ||
              !onViewExecution
            }
            onClick={() => {

              if (
                fullExecution &&
                onViewExecution
              ) {

                onViewExecution(
                  fullExecution
                );
              }
            }}
          >
            View Execution
          </button>

        </div>

      )}

    </article>
  );
}

function TraceabilityTestCase({
  testCase,
  executions,
  onViewExecution
}) {
  const occurrences =
    Array.isArray(
      testCase.occurrences
    )
      ? testCase.occurrences
      : [];


  return (
    <article className="traceability-test-case">

      <div className="traceability-test-header">

        <div>

          <span className="requirement-id">
            {testCase.test_case_id}
          </span>

          <h4>
            {testCase.title}
          </h4>

        </div>


        <span className="traceability-history-count">
          {occurrences.length}
          {" "}
          {occurrences.length === 1
            ? "Cycle"
            : "Cycles"}
        </span>

      </div>


      <div className="traceability-test-meta">

        {testCase.test_type && (

          <span>
            {testCase.test_type
              .toUpperCase()}
          </span>

        )}


        {testCase.priority && (

          <span>
            {testCase.priority
              .toUpperCase()}
            {" "}
            PRIORITY
          </span>

        )}


        {testCase.current_execution_type && (

          <span>
            CURRENT:
            {" "}
            {testCase
              .current_execution_type
              .toUpperCase()}
          </span>

        )}

      </div>


      {occurrences.length === 0 ? (

        <div className="traceability-not-covered">

          Not yet included in a Test Cycle.

        </div>

      ) : (

        <div className="traceability-occurrence-list">

          {occurrences.map(
            (occurrence) => (

              <TraceabilityOccurrence
  key={
    occurrence.cycle_item_id
  }

  occurrence={
    occurrence
  }

  executions={
    executions
  }

  onViewExecution={
    onViewExecution
  }
/>

            )
          )}

        </div>

      )}

    </article>
  );
}

function TraceabilityOccurrence({
  occurrence,
  executions,
  onViewExecution
}) {
  const status = String(
  occurrence.result_status ||
  "not_run"
).toLowerCase();


  const execution =
    occurrence.execution;

  const fullExecution =
  execution
    ? (
        executions || []
      ).find(
        (item) =>
          item.id ===
          execution.id
      )
    : null;


  return (
    <div className="traceability-occurrence">

      <div className="traceability-occurrence-heading">

        <div>

          <strong>
            {occurrence.cycle_name}
          </strong>

          <span>
            Cycle #{occurrence.cycle_id}
          </span>

        </div>


        <span
          className={
            `cycle-item-status cycle-item-status-${status}`
          }
        >
          {status
            .replaceAll(
              "_",
              " "
            )
            .toUpperCase()}
        </span>

      </div>


      <div className="traceability-occurrence-meta">

        <span>
          {(
            occurrence.execution_mode ||
            "unknown"
          ).toUpperCase()}
        </span>

        <span>
  CYCLE:
  {" "}
  {(
    occurrence.cycle_status ||
    "unknown"
  )
    .replaceAll(
      "_",
      " "
    )
    .toUpperCase()}
</span>


        {occurrence.release && (

          <span>
            Release:
            {" "}
            {occurrence.release}
          </span>

        )}


        {occurrence.environment && (

          <span>
            Environment:
            {" "}
            {occurrence.environment}
          </span>

        )}


        {occurrence.automation_version_id !=
  null && (

          <span>
            Frozen Automation:
            {" "}

            {occurrence.automation_engine
              ? occurrence
                  .automation_engine
                  .toUpperCase()
              : "AUTOMATION"}

            {occurrence
              .automation_version_number !==
              null &&
              occurrence
                .automation_version_number !==
                undefined && (
                <>
                  {" "}
                  V
                  {occurrence
                    .automation_version_number}
                </>
              )}
          </span>

        )}


        {execution && (

          <span>
            Execution:
            {" "}
            #{execution.id}
          </span>

        )}

      </div>


      {occurrence.actual_result && (

        <div className="traceability-result-detail">

          <strong>
            Actual Result
          </strong>

          <p>
            {occurrence.actual_result}
          </p>

        </div>

      )}


      {occurrence.comment && (

        <div className="traceability-result-detail">

          <strong>
            Comment
          </strong>

          <p>
            {occurrence.comment}
          </p>

        </div>

      )}


      {occurrence.defect_reference && (

        <div className="traceability-result-detail">

          <strong>
            Defect
          </strong>

          <p>
            {occurrence.defect_reference}
          </p>

        </div>

      )}


      {execution && (

        <div className="traceability-evidence-tags">

          <span>
      Execution Status:
      {" "}
      {(
        execution.status ||
        "unknown"
      ).toUpperCase()}
    </span>

          <span>
            Exit Code:
            {" "}
            {execution.exit_code ??
              "N/A"}
          </span>


          <span>
            Duration:
            {" "}
            {execution.duration_ms !==
              null &&
              execution.duration_ms !==
              undefined
              ? `${execution.duration_ms} ms`
              : "N/A"}
          </span>


          {execution.screenshot_available && (

            <span className="traceability-evidence-available">
              SCREENSHOT
            </span>

          )}


          {execution.trace_available && (

            <span className="traceability-evidence-available">
              TRACE
            </span>

          )}

        </div>

      )}

      {execution && (

  <div className="traceability-occurrence-actions">

    <button
      type="button"
      className="secondary-button"
      disabled={
        !fullExecution ||
        !onViewExecution
      }
      onClick={() => {
        if (
          fullExecution &&
          onViewExecution
        ) {

          onViewExecution(
            fullExecution
          );
        }
      }}
    >
      View Execution
    </button>

  </div>

)}

    </div>
  );
}

function ReportMetric({
  label,
  value,
  tone = "default",
  featured = false
}) {
  return (
    <article
      className={
        `report-metric report-${tone} ${
          featured
            ? "report-metric-featured"
            : ""
        }`
      }
    >

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </article>
  );
}


function getPassRateTone(
  passRate
) {
  if (passRate >= 80) {
    return "success";
  }

  if (passRate >= 50) {
    return "warning";
  }

  if (passRate > 0) {
    return "danger";
  }

  return "neutral";
}


function QualitySignal({
  summary
}) {
  if (summary.executions === 0) {
    return (
      <div className="quality-signal quality-signal-neutral">

        <strong>
          No execution signal yet
        </strong>

        <p>
          Run READY automation to establish
          execution quality.
        </p>

      </div>
    );
  }


  if (summary.errors > 0) {
    return (
      <div className="quality-signal quality-signal-warning">

        <strong>
          Execution errors detected
        </strong>

        <p>
          Review execution errors separately
          from assertion failures.
        </p>

      </div>
    );
  }


  if (summary.pass_rate >= 80) {
    return (
      <div className="quality-signal quality-signal-success">

        <strong>
          Strong execution signal
        </strong>

        <p>
          Most completed test executions are
          currently passing.
        </p>

      </div>
    );
  }


  return (
    <div className="quality-signal quality-signal-danger">

      <strong>
        Execution failures need attention
      </strong>

      <p>
        Review failed executions and their
        captured evidence.
      </p>

    </div>
  );
}

function CoverageMetric({
  label,
  value
}) {
  return (
    <div className="coverage-metric">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


function CoverageStatus({
  status
}) {
  if (!status) {
    return (
      <span className="coverage-status coverage-not-run">
        NOT RUN
      </span>
    );
  }

  return (
    <span
      className={
        `coverage-status coverage-${status}`
      }
    >
      {status.toUpperCase()}
    </span>
  );
}

function ExecutionTrendItem({
  execution
}) {
  const status =
    execution.status ||
    "unknown";


  const duration =
    execution.duration_ms !== null &&
    execution.duration_ms !== undefined
      ? formatDuration(
          execution.duration_ms
        )
      : "N/A";


  return (
    <article className="execution-trend-item">

      <div className="execution-trend-main">

        <div className="execution-trend-heading">

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

      </div>


      <div className="execution-trend-duration">

        <span>
          Duration
        </span>

        <strong>
          {duration}
        </strong>

      </div>

    </article>
  );
}

function formatDuration(
  durationMs
) {
  if (
    durationMs === null ||
    durationMs === undefined
  ) {
    return "N/A";
  }

  if (durationMs < 1000) {
    return `${durationMs} ms`;
  }

  return `${
    (
      durationMs /
      1000
    ).toFixed(1)
  } s`;
}

export default ReportsPage;