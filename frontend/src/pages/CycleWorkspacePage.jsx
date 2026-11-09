function CycleWorkspacePage({
  cycle,
  summary,
  loading = false,
  actionLoading = false,
  runningItemId = null,
  onBack,
  onRefresh,
  onChangeStatus,
  onOpenManualResult,
  onRunAutomation,
  onOpenExecution
}) {
  if (loading) {
    return (
      <section className="cycle-workspace-page">

        <div className="api-status">
          Loading Test Cycle...
        </div>

      </section>
    );
  }


  if (!cycle) {
    return (
      <section className="cycle-workspace-page">

        <div className="empty-state">

          <h4>
            Test Cycle not loaded
          </h4>

          <p>
            Return to Test Cycles and open
            a Cycle.
          </p>

          <button
            type="button"
            className="secondary-button"
            onClick={onBack}
          >
            Back to Test Cycles
          </button>

        </div>

      </section>
    );
  }


  const items =
    Array.isArray(cycle.items)
      ? [...cycle.items].sort(
          (left, right) =>
            left.position -
            right.position
        )
      : [];


  const manualItems =
    items.filter(
      (item) =>
        item.execution_mode ===
        "manual"
    );


  const automationItems =
    items.filter(
      (item) =>
        item.execution_mode ===
        "automation"
    );


  const cycleStatus =
    cycle.status ||
    "draft";


  const canRecordResults =
    cycleStatus ===
    "in_progress";


  const canComplete =
    canRecordResults &&
    summary?.completion_eligible ===
      true;


  return (
    <section className="cycle-workspace-page">

      <div className="workspace-header">

        <div>

          <button
            type="button"
            className="back-button"
            onClick={onBack}
          >
            ← Back to Test Cycles
          </button>


          <span className="section-label">
            TEST CYCLE
          </span>


          <h3>
            {cycle.name}
          </h3>


          <p>
            Execute Manual and Automated
            Test Cases from this frozen
            Cycle plan.
          </p>


          <div className="workspace-tags">

            <span>
              CYCLE #{cycle.id}
            </span>

            <span>
              {cycleStatus
                .replaceAll(
                  "_",
                  " "
                )
                .toUpperCase()}
            </span>

            <span>
              Release:
              {" "}
              {cycle.release ||
                "Not specified"}
            </span>

            <span>
              Environment:
              {" "}
              {cycle.environment ||
                "Not specified"}
            </span>

          </div>

        </div>


        <div className="cycle-header-actions">

          <button
            type="button"
            className="secondary-button"
            disabled={
              actionLoading
            }
            onClick={onRefresh}
          >
            Refresh
          </button>


          {cycleStatus === "draft" && (

            <button
              type="button"
              className="primary-button"
              disabled={
                actionLoading
              }
              onClick={() =>
                onChangeStatus(
                  "ready"
                )
              }
            >
              Mark Ready
            </button>

          )}


          {cycleStatus === "ready" && (

            <button
              type="button"
              className="primary-button"
              disabled={
                actionLoading
              }
              onClick={() =>
                onChangeStatus(
                  "in_progress"
                )
              }
            >
              Start Cycle
            </button>

          )}


          {cycleStatus ===
            "in_progress" && (

            <button
              type="button"
              className="primary-button"
              disabled={
                actionLoading ||
                !canComplete
              }
              onClick={() =>
                onChangeStatus(
                  "completed"
                )
              }
            >
              Complete Cycle
            </button>

          )}

        </div>

      </div>


      <div className="cycle-summary-grid">

        <CycleSummaryMetric
          label="Total"
          value={
            summary?.total ?? 0
          }
        />

        <CycleSummaryMetric
          label="Completed"
          value={
            summary?.completed ?? 0
          }
        />

        <CycleSummaryMetric
          label="Passed"
          value={
            summary?.passed ?? 0
          }
        />

        <CycleSummaryMetric
          label="Failed"
          value={
            summary?.failed ?? 0
          }
        />

        <CycleSummaryMetric
          label="Blocked"
          value={
            summary?.blocked ?? 0
          }
        />

        <CycleSummaryMetric
          label="Skipped"
          value={
            summary?.skipped ?? 0
          }
        />

        <CycleSummaryMetric
          label="Error"
          value={
            summary?.error ?? 0
          }
        />

        <CycleSummaryMetric
          label="Not Run"
          value={
            summary?.not_run ?? 0
          }
        />

      </div>


      {cycleStatus ===
        "in_progress" &&
        !canComplete && (

        <div className="analysis-notice">
          Complete every Manual and Automated
          Cycle item before completing this
          Test Cycle.
        </div>

      )}


      {cycleStatus === "completed" && (

        <div className="analysis-notice">
          This Test Cycle is completed and
          read-only. Stored results,
          automation versions, Executions
          and evidence remain available.
        </div>

      )}


      <CycleItemSection
        title="Manual Test Cases"
        emptyMessage={
          "This Cycle does not contain Manual Test Cases."
        }
        items={manualItems}
        cycleStatus={cycleStatus}
        runningItemId={
          runningItemId
        }
        onOpenManualResult={
          onOpenManualResult
        }
        onRunAutomation={
          onRunAutomation
        }
        onOpenExecution={
          onOpenExecution
        }
      />


      <CycleItemSection
        title="Automated Test Cases"
        emptyMessage={
          "This Cycle does not contain Automated Test Cases."
        }
        items={automationItems}
        cycleStatus={cycleStatus}
        runningItemId={
          runningItemId
        }
        onOpenManualResult={
          onOpenManualResult
        }
        onRunAutomation={
          onRunAutomation
        }
        onOpenExecution={
          onOpenExecution
        }
      />

    </section>
  );
}


function CycleItemSection({
  title,
  emptyMessage,
  items,
  cycleStatus,
  runningItemId,
  onOpenManualResult,
  onRunAutomation,
  onOpenExecution
}) {
  return (
    <section className="cycle-item-section">

      <div className="panel-header">

        <div>

          <span className="section-label">
            EXECUTION
          </span>

          <h3>
            {title}
          </h3>

        </div>


        <span className="cycle-item-count">
          {items.length}
        </span>

      </div>


      {items.length === 0 ? (

        <div className="empty-state">

          <p>
            {emptyMessage}
          </p>

        </div>

      ) : (

        <div className="cycle-workspace-item-list">

          {items.map(
            (item) => (

              <article
                className="cycle-workspace-item"
                key={item.id}
              >

                <div className="cycle-workspace-item-main">

                  <div>

                    <div className="generated-test-heading">

                      <span className="requirement-id">
  {item.test_case_key}
</span>


<span className="cycle-internal-id">
  Cycle Item #{item.id}
</span>

                      <span
                        className={
                          `cycle-item-status cycle-item-status-${
                            item.status ||
                            "not_run"
                          }`
                        }
                      >
                        {(
                          item.status ||
                          "not_run"
                        )
                          .replaceAll(
                            "_",
                            " "
                          )
                          .toUpperCase()}
                      </span>

                    </div>


                    <h4>
  {item.test_case_title}
</h4>


                    <div className="cycle-item-meta">

  <span>
    {(
  item.execution_mode ||
  "unknown"
).toUpperCase()}
  </span>


  <span>
    Position:
    {" "}
    {item.position}
  </span>


  {item.execution_mode ===
    "automation" &&
    item.automation_version_id !==
      null && (

    <span>
      Frozen Automation:
      {" "}

      {item.automation_engine
        ? item.automation_engine
            .toUpperCase()
        : "AUTOMATION"}

      {item.automation_version_number !==
        null &&
        item.automation_version_number !==
        undefined && (
        <>
          {" "}
          V
          {item.automation_version_number}
        </>
      )}
    </span>

  )}


  {item.automation_language && (

    <span>
      {item.automation_language
        .toUpperCase()}
    </span>

  )}


  {item.execution_id !==
    null && (

    <span>
      Execution:
      {" "}
      #{item.execution_id}
    </span>

  )}

</div>


                    {item.actual_result && (

                      <div className="cycle-result-text">

                        <strong>
                          Actual Result
                        </strong>

                        <p>
                          {item.actual_result}
                        </p>

                      </div>

                    )}


                    {item.comment && (

                      <div className="cycle-result-text">

                        <strong>
                          Comment
                        </strong>

                        <p>
                          {item.comment}
                        </p>

                      </div>

                    )}


                    {item.defect_reference && (

                      <div className="cycle-result-text">

                        <strong>
                          Defect
                        </strong>

                        <p>
                          {item.defect_reference}
                        </p>

                      </div>

                    )}

                  </div>


                  <div className="cycle-item-actions">

                    {item.execution_mode ===
                      "manual" &&
                      cycleStatus ===
                        "in_progress" && (

                      <button
                        type="button"
                        className="primary-button"
                        onClick={() =>
                          onOpenManualResult(
                            item
                          )
                        }
                      >
                        {item.status ===
                          "not_run"
                          ? "Record Result"
                          : "Update Result"}
                      </button>

                    )}


                    {item.execution_mode ===
                      "automation" &&
                      cycleStatus ===
                        "in_progress" &&
                      item.status ===
                        "not_run" && (

                      <button
                        type="button"
                        className="primary-button"
                        disabled={
                          runningItemId ===
                          item.id
                        }
                        onClick={() =>
                          onRunAutomation(
                            item
                          )
                        }
                      >
                        {runningItemId ===
                          item.id
                          ? "Preparing..."
                          : "Run Automation"}
                      </button>

                    )}


                    {item.execution_id !==
                      null && (

                      <button
                        type="button"
                        className="secondary-button"
                        onClick={() =>
                          onOpenExecution(
                            item
                          )
                        }
                      >
                        View Execution
                      </button>

                    )}

                  </div>

                </div>

              </article>

            )
          )}

        </div>

      )}

    </section>
  );
}


function CycleSummaryMetric({
  label,
  value
}) {
  return (
    <article className="metric-card">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </article>
  );
}


export default CycleWorkspacePage;