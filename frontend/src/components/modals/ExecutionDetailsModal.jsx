function ExecutionDetailsModal({
  execution,
  screenshotUrl,
  screenshotLoading,
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

          </div>


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


export default ExecutionDetailsModal;