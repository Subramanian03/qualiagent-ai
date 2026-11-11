function ExecutionDetailsModal({
  execution,
  screenshotUrl,
  screenshotLoading,
  failureAnalysis,
failureAnalysisLoading = false,
failureAnalysisError = "",
onAnalyzeFailure,
  onViewScreenshot,
  onDownloadTrace,
  onClose
}) {
  if (!execution) {
    return null;
  }


  const status =
    execution.status ||
    "unknown";


  const duration =
    execution.duration_ms !== null &&
    execution.duration_ms !== undefined
      ? `${execution.duration_ms} ms`
      : "N/A";


  const exitCode =
    execution.exit_code !== null &&
    execution.exit_code !== undefined
      ? execution.exit_code
      : "N/A";


  function formatDate(value) {
    if (!value) {
      return "N/A";
    }

    const date =
      new Date(value);

    if (
      Number.isNaN(
        date.getTime()
      )
    ) {
      return value;
    }

    return date.toLocaleString();
  }

  const executionStatus = String(
  execution?.status ||
  ""
).trim().toLowerCase();


const canAnalyzeFailure =
  executionStatus === "failed" ||
  executionStatus === "error";

  return (
    <div className="modal-backdrop">

      <div className="modal-card execution-details-modal">

        <div className="modal-header">

          <div>

            <span className="section-label">
              EXECUTION DETAILS
            </span>

            <h3>
              Execution #{execution.id}
            </h3>

            <p className="modal-subtitle">
              {execution.test_case_id ||
                "Unknown test case"}
            </p>

          </div>


          <button
            type="button"
            className="modal-close"
            onClick={onClose}
          >
            ×
          </button>

        </div>


        <div className="execution-details-tags">

          <span
            className={
              `execution-status execution-${status}`
            }
          >
            {status.toUpperCase()}
          </span>

          <span>
            {(execution.framework ||
              "unknown")
              .toUpperCase()}
          </span>

          <span>
            {(execution.language ||
              "unknown")
              .toUpperCase()}
          </span>

        </div>


        <section className="execution-detail-section">

          <h4>
            Test Case
          </h4>

          <strong>
            {execution.test_case_title ||
              "Untitled test case"}
          </strong>

          <p>
            {execution.test_case_id ||
              "Unknown test case"}

            {" · "}

            {execution.requirement_id ||
              "Unknown requirement"}
          </p>

        </section>


        <div className="execution-detail-grid">

          <ExecutionDetailItem
            label="Status"
            value={
              status.toUpperCase()
            }
          />

          <ExecutionDetailItem
            label="Exit Code"
            value={exitCode}
          />

          <ExecutionDetailItem
            label="Duration"
            value={duration}
          />

          <ExecutionDetailItem
            label="Started"
            value={
              formatDate(
                execution.started_at
              )
            }
          />

          <ExecutionDetailItem
            label="Completed"
            value={
              formatDate(
                execution.completed_at
              )
            }
          />

          <ExecutionDetailItem
            label="Created"
            value={
              formatDate(
                execution.created_at
              )
            }
          />

        </div>


        {execution.error_message && (

          <section className="execution-detail-section">

            <h4>
              Failure / Error
            </h4>

            <div className="api-error">
              {execution.error_message}
            </div>

          </section>

        )}


        {execution.stdout && (

          <section className="execution-detail-section">

            <h4>
              Playwright Output
            </h4>

            <pre className="execution-history-output">
              {execution.stdout}
            </pre>

          </section>

        )}


        {execution.stderr && (

          <section className="execution-detail-section">

            <h4>
              Error Output
            </h4>

            <pre className="execution-history-output execution-history-error-output">
              {execution.stderr}
            </pre>

          </section>

        )}


        <section className="execution-detail-section">

          <h4>
            Evidence
          </h4>


          <div className="execution-evidence-status">

            <span>
              Screenshot
            </span>

            <strong>
              {execution.screenshot_path
                ? "Available"
                : "Not Available"}
            </strong>

          </div>


          <div className="execution-evidence-status">

            <span>
              Playwright Trace
            </span>

            <strong>
              {execution.trace_path
                ? "Available"
                : "Not Available"}
            </strong>

          </div>


          <div className="execution-evidence-actions">

  {execution.screenshot_path && (

    <button
      type="button"
      className="secondary-button"
      disabled={
        screenshotLoading
      }
      onClick={
        onViewScreenshot
      }
    >
      {screenshotLoading
        ? "Loading..."
        : "View Screenshot"}
    </button>

  )}


  {execution.trace_path && (

    <button
      type="button"
      className="secondary-button"
      onClick={
        onDownloadTrace
      }
    >
      Download Trace
    </button>

  )}


  {canAnalyzeFailure && (

    <button
      type="button"
      className="primary-button"
      disabled={
        failureAnalysisLoading ||
        !onAnalyzeFailure
      }
      onClick={
        onAnalyzeFailure
      }
    >
      {failureAnalysisLoading
        ? "Analyzing..."
        : failureAnalysis
          ? "Analyze Again"
          : "Analyze Failure with AI"}
    </button>

  )}

</div>

         {failureAnalysisError && (

  <div
    className="failure-analysis-error"
    role="alert"
  >
    {failureAnalysisError}
  </div>

)}


          {screenshotUrl && (

  <div className="execution-screenshot">

    <img
      src={screenshotUrl}
      alt={
        `Execution ${execution.id} failure evidence`
      }
    />

  </div>

)}

        </section>


{failureAnalysis && (

  <FailureAnalysisPanel
    analysis={
      failureAnalysis
    }
  />

)}


<div className="execution-details-footer">

          <span>
            Execution results are read-only
            historical records.
          </span>

          <button
            type="button"
            className="primary-button"
            onClick={onClose}
          >
            Close
          </button>

        </div>

      </div>

    </div>
  );
}


function ExecutionDetailItem({
  label,
  value
}) {
  return (
    <div className="execution-detail-item">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}

function FailureAnalysisPanel({
  analysis
}) {
  const finding =
    analysis?.finding;


  const suggestion =
    analysis?.suggested_automation_change;


  const classification = String(
    finding?.classification ||
    "unknown"
  ).toLowerCase();


  const recommendationType = String(
    finding?.recommendation_type ||
    "manual_investigation"
  );


  const confidenceValue =
    Number(
      finding?.confidence
    );


  const confidencePercent =
    Number.isFinite(
      confidenceValue
    )
      ? Math.round(
          Math.max(
            0,
            Math.min(
              1,
              confidenceValue
            )
          ) * 100
        )
      : 0;


  const evidenceItems =
    Array.isArray(
      finding?.evidence
    )
      ? finding.evidence
      : [];


  return (
    <section className="failure-analysis-panel">

      <div className="failure-analysis-heading">

        <div>

          <span className="section-label">
            AI FAILURE ANALYSIS
          </span>

          <h3>
            Failure diagnosis
          </h3>

        </div>


        <div className="failure-analysis-badges">

          <span
            className={
              `failure-analysis-classification failure-analysis-${classification}`
            }
          >
            {classification
              .replaceAll(
                "_",
                " "
              )
              .toUpperCase()}
          </span>


          <span className="failure-analysis-confidence">
            {confidencePercent}%
            {" "}
            confidence
          </span>

        </div>

      </div>


      <div className="failure-analysis-warning">

        <strong>
          Human review required
        </strong>

        <p>
          This diagnosis is advisory. It did
          not change the historical Execution
          result or modify the frozen
          Automation version.
        </p>

      </div>


      <div className="failure-analysis-detail">

        <strong>
          Summary
        </strong>

        <p>
          {finding?.summary ||
            "No summary returned."}
        </p>

      </div>


      <div className="failure-analysis-detail">

        <strong>
          Likely cause
        </strong>

        <p>
          {finding?.likely_cause ||
            "No likely cause returned."}
        </p>

      </div>


      <div className="failure-analysis-detail">

        <strong>
          Supporting evidence
        </strong>

        {evidenceItems.length === 0 ? (

          <p>
            No supporting evidence returned.
          </p>

        ) : (

          <ul>

            {evidenceItems.map(
              (
                item,
                index
              ) => (

                <li
                  key={
                    `${index}-${item}`
                  }
                >
                  {item}
                </li>

              )
            )}

          </ul>

        )}

      </div>


      <div className="failure-analysis-detail">

        <strong>
          Recommended action
        </strong>

        <span className="failure-analysis-recommendation-type">
          {recommendationType
            .replaceAll(
              "_",
              " "
            )
            .toUpperCase()}
        </span>

        <p>
          {finding?.recommended_action ||
            "No recommended action returned."}
        </p>

      </div>


      {suggestion && (

        <div className="failure-analysis-suggestion">

          <div>

            <strong>
              Suggested automation change
            </strong>

            <span>
              {suggestion.applicable
                ? "APPLICABLE"
                : "NOT APPLICABLE"}
            </span>

          </div>


          <p>
            {suggestion.rationale}
          </p>


          {suggestion.current_code_excerpt && (

            <div className="failure-analysis-code">

              <strong>
                Current code excerpt
              </strong>

              <pre>
                {suggestion
                  .current_code_excerpt}
              </pre>

            </div>

          )}


          {suggestion.suggested_code_excerpt && (

            <div className="failure-analysis-code">

              <strong>
                Suggested code excerpt
              </strong>

              <pre>
                {suggestion
                  .suggested_code_excerpt}
              </pre>

            </div>

          )}


          {suggestion.full_replacement_code && (

            <div className="failure-analysis-code">

              <strong>
                Suggested replacement
              </strong>

              <pre>
                {suggestion
                  .full_replacement_code}
              </pre>

            </div>

          )}

        </div>

      )}


      <div className="failure-analysis-provider">

        <span>
          Provider:
          {" "}
          {analysis?.provider?.provider ||
            "unknown"}
        </span>

        <span>
          Model:
          {" "}
          {analysis?.provider?.model ||
            "N/A"}
        </span>

        <span>
          Mode:
          {" "}
          {analysis?.provider?.mode ||
            "unknown"}
        </span>

      </div>

    </section>
  );
}


export default ExecutionDetailsModal;