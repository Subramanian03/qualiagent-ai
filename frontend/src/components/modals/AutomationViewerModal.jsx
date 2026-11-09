import {
  useEffect,
  useState
} from "react";

function AutomationViewerModal({
  automation,
  testCase,
  history = [],
  historyLoading = false,
  reviewing = false,
  savingEdit = false,
  updatingWithAI = false,
  onSaveEdit,
  onUpdateWithAI,
  onApprove,
  onReject,
  onClose
}) {
  const [editing, setEditing] = useState(false);

  const [editedCode,setEditedCode] = useState("");

  const [changeSummary,setChangeSummary] = useState("");

  const [updatingAI,setUpdatingAI] = useState(false);

  const [aiInstruction,setAIInstruction] = useState("");

  const [showHistory,setShowHistory] = useState(false);

  const [historyVersion,setHistoryVersion] = useState(null);


useEffect(() => {

  setEditedCode(
    automation?.code || ""
  );

  setChangeSummary("");

  setAIInstruction("");

  setEditing(false);

  setUpdatingAI(false);

  setHistoryVersion(null);

}, [
  automation?.id
]);
  if (!automation || !testCase) {
    return null;
  }

  const status =
    (
      automation.status ||
      "draft"
    ).toLowerCase();

  const isDraft =
    status === "draft";

  const isReady =
    status === "ready";

  const isRejected =
    status === "rejected";

  const isLegacy =
  (
    automation.source ||
    ""
  ).toLowerCase() ===
    "legacy" ||
  !automation.input_schema;

  const framework =
    automation.framework ||
    "playwright";

  const language =
    automation.language ||
    "javascript";

  const code =
    automation.code ||
    "// No automation code generated yet.";

function beginEditing() {

  setEditedCode(
    automation.code || ""
  );

  setChangeSummary("");

  setEditing(true);
}


function cancelEditing() {

  setEditedCode(
    automation.code || ""
  );

  setChangeSummary("");

  setEditing(false);
}

function beginAIUpdate() {

  setAIInstruction("");

  setUpdatingAI(true);
}


function cancelAIUpdate() {

  setAIInstruction("");

  setUpdatingAI(false);
}


async function submitAIUpdate(
  event
) {
  event.preventDefault();


  if (
    typeof onUpdateWithAI !==
    "function"
  ) {
    return;
  }


  await onUpdateWithAI(
    aiInstruction
  );
}


async function saveEditing(
  event
) {
  event.preventDefault();


  if (
    typeof onSaveEdit !==
    "function"
  ) {
    return;
  }


  await onSaveEdit(
    editedCode,
    changeSummary
  );
}


  return (
    <div className="modal-backdrop">

      <div className="modal-card automation-viewer-modal">

        {/* HEADER */}
        <div className="modal-header">

          <div>

            <span className="section-label">
              AUTOMATION SOURCE
            </span>

            <h3>
              {testCase.title}
            </h3>

            <p className="modal-subtitle">
              {testCase.test_case_id}
            </p>

          </div>


          <button
  type="button"
  className="modal-close"
  disabled={
    reviewing ||
    savingEdit ||
    updatingWithAI
  }
  onClick={
    updatingAI
      ? cancelAIUpdate
      : onClose
  }
>
  ×
</button>

        </div>


        {/* AUTOMATION TAGS */}
        <div className="automation-viewer-tags">

  <span>
    {framework.toUpperCase()}
  </span>


  <span>
    {language.toUpperCase()}
  </span>


  <span>
    VERSION {
      automation.version || 1
    }
  </span>


  <span>
    {(automation.source ||
      "unknown")
      .replaceAll(
        "_",
        " "
      )
      .toUpperCase()}
  </span>


  <span
    className={
      `automation-state automation-state-${status}`
    }
  >
    {status.toUpperCase()}
  </span>

</div>

        {automation.change_summary && (

  <div className="automation-change-summary">

    <strong>
      Change Summary
    </strong>

    <p>
      {automation.change_summary}
    </p>

  </div>

)}

        {isLegacy && (

  <div
    className={
      "automation-review-message "
      + "automation-review-draft"
    }
  >

    <strong>
      Legacy automation version
    </strong>

    <p>
      This automation was created before
      runtime input schemas were persisted.
      Generate a new automation version
      before using Edit Code or
      Update with AI.
    </p>

  </div>

)}


        {/* HUMAN REVIEW STATUS */}
        <div
          className={
            `automation-review-message automation-review-${status}`
          }
        >

          {isDraft && !isLegacy && (
            <>
              <strong>
                Human review required
              </strong>

              <p>
  Review this automation version
  before approving it for execution.
</p>
            </>
          )}


          {isReady && !isLegacy && (
            <>
              <strong>
                Approved for execution
              </strong>

              <p>
                This automation has passed the
                human review gate.
              </p>
            </>
          )}


          {isRejected && !isLegacy && (
            <>
              <strong>
                Automation rejected
              </strong>

              <p>
                This generated script is not
                eligible for execution.
              </p>
            </>
          )}

        </div>


        {/* EXECUTION NOTICE */}
        <div className="automation-execution-notice">

          <strong>
  AUTOMATION VERSION • REVIEWED EXECUTION ONLY
</strong>

          <p>
  This version is stored independently.
  Only a READY automation version is
  eligible for execution.
</p>

        </div>


        {/* PLAYWRIGHT SOURCE */}
        <div className="automation-code-section">

  <div className="automation-code-header">

    <span>
      {framework.toUpperCase()}
      {" "}
      {language.toUpperCase()}
    </span>

    <span>
      {editing
        ? "Editing new version"
        : "Read-only"}
    </span>

  </div>


  {editing ? (

    <form
      onSubmit={saveEditing}
      className="automation-edit-form"
    >

      <div className="form-field">

        <label
          htmlFor="automation-code-editor"
        >
          Automation Code
        </label>

        <textarea
          id="automation-code-editor"
          className="automation-code-editor"
          required
          minLength="20"
          value={editedCode}
          disabled={savingEdit}
          onChange={(event) =>
            setEditedCode(
              event.target.value
            )
          }
          spellCheck="false"
        />

      </div>


      <div className="form-field">

        <label
          htmlFor="automation-change-summary"
        >
          Change Summary
        </label>

        <textarea
          id="automation-change-summary"
          required
          minLength="3"
          maxLength="500"
          rows="3"
          value={changeSummary}
          disabled={savingEdit}
          onChange={(event) =>
            setChangeSummary(
              event.target.value
            )
          }
          placeholder={
            "Describe what you changed and why"
          }
        />

      </div>


      <div className="form-actions">

        <button
          type="button"
          className="secondary-button"
          disabled={savingEdit}
          onClick={cancelEditing}
        >
          Cancel Edit
        </button>


        <button
          type="submit"
          className="primary-button"
          disabled={savingEdit}
        >
          {savingEdit
            ? "Saving Draft..."
            : "Save as New Draft"}
        </button>

      </div>

    </form>

  ) : (

    <pre className="automation-code">
      <code>
        {code}
      </code>
    </pre>

  )}

</div>

        {/* AI UPDATE FORM */}
{updatingAI && (

  <form
    className="automation-ai-update-form"
    onSubmit={submitAIUpdate}
  >

    <div className="form-field">

      <label
        htmlFor="automation-ai-instruction"
      >
        AI Update Instruction
      </label>


      <textarea
        id="automation-ai-instruction"
        required
        minLength="5"
        maxLength="2000"
        rows="5"
        value={aiInstruction}
        disabled={updatingWithAI}
        onChange={(event) =>
          setAIInstruction(
            event.target.value
          )
        }
        placeholder={
          "Example: Improve locator reliability and strengthen the successful login assertion."
        }
      />


      <small>
        AI will create a new DRAFT
        automation version. The currently
        approved READY version will remain
        unchanged until this new version is
        reviewed and approved.
      </small>

    </div>


    <div className="form-actions">

      <button
        type="button"
        className="secondary-button"
        disabled={updatingWithAI}
        onClick={cancelAIUpdate}
      >
        Cancel
      </button>


      <button
        type="submit"
        className="primary-button"
        disabled={
          updatingWithAI ||
          aiInstruction.trim().length < 5
        }
      >
        {updatingWithAI
          ? "Updating with AI..."
          : "Generate Updated Draft"}
      </button>

    </div>

  </form>

)}


{/* AUTOMATION VERSION HISTORY */}
{showHistory && (

  <div className="automation-history">

    <div className="automation-history-header">

      <div>

        <span className="section-label">
          VERSION HISTORY
        </span>

        <h4>
          Automation Versions
        </h4>

      </div>

    </div>


    {historyLoading ? (

      <div className="api-status">
        Loading version history...
      </div>

    ) : history.length === 0 ? (

      <div className="empty-state">

        <p>
          No automation versions found.
        </p>

      </div>

    ) : historyVersion ? (

      <div className="automation-history-detail">

        <div className="automation-history-detail-header">

          <div>

            <strong>
              Version {
                historyVersion.version
              }
            </strong>

            <span>
              {" · "}
              {
                (
                  historyVersion.source ||
                  "unknown"
                )
                .replaceAll(
                  "_",
                  " "
                )
                .toUpperCase()
              }
            </span>

          </div>


          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              setHistoryVersion(
                null
              )
            }
          >
            Back to History
          </button>

        </div>


        <div className="automation-viewer-tags">

          <span>
            VERSION {
              historyVersion.version
            }
          </span>

          <span>
            {
              (
                historyVersion.status ||
                "unknown"
              ).toUpperCase()
            }
          </span>

          <span>
            {
              (
                historyVersion.source ||
                "unknown"
              )
              .replaceAll(
                "_",
                " "
              )
              .toUpperCase()
            }
          </span>

        </div>


        {historyVersion.change_summary && (

          <div className="automation-change-summary">

            <strong>
              Change Summary
            </strong>

            <p>
              {
                historyVersion
                  .change_summary
              }
            </p>

          </div>

        )}


        <div className="analysis-notice">
          This historical automation
          version is read-only.
        </div>


        <pre className="automation-code">
          <code>
            {
              historyVersion.code ||
              "// No code stored."
            }
          </code>
        </pre>

      </div>

    ) : (

      <div className="automation-history-list">

        {history.map(
          (version) => (

            <article
              className="automation-history-item"
              key={version.id}
            >

              <div>

                <div className="automation-history-title">

                  <strong>
                    Version {
                      version.version
                    }
                  </strong>

                  <span>
                    {
                      (
                        version.status ||
                        "unknown"
                      ).toUpperCase()
                    }
                  </span>

                </div>


                <p>
                  {
                    (
                      version.source ||
                      "unknown"
                    )
                    .replaceAll(
                      "_",
                      " "
                    )
                    .toUpperCase()
                  }
                </p>


                {version.change_summary && (

                  <small>
                    {
                      version.change_summary
                    }
                  </small>

                )}

              </div>


              <button
                type="button"
                className="secondary-button"
                onClick={() =>
                  setHistoryVersion(
                    version
                  )
                }
              >
                View
              </button>

            </article>

          )
        )}

      </div>

    )}

  </div>

)}


        {/* TEST CASE REFERENCE */}
        <div className="automation-viewer-footer">

          <div>

            <span className="section-label">
              TEST CASE
            </span>

            <strong>
              {testCase.test_case_id}
            </strong>

          </div>

        </div>


        {/* HUMAN REVIEW ACTIONS */}
        <div className="automation-review-actions">
          
          {!editing &&
  !updatingAI &&
  !showHistory &&
  !isLegacy && (
  <>
    <button
      type="button"
      className="secondary-button"
      disabled={
        reviewing ||
        savingEdit ||
        updatingWithAI
      }
      onClick={
        beginEditing
      }
    >
      Edit Code
    </button>


    <button
      type="button"
      className="secondary-button"
      disabled={
        reviewing ||
        savingEdit ||
        updatingWithAI
      }
      onClick={
        beginAIUpdate
      }
    >
      Update with AI
    </button>
  </>
)}

          {!editing &&
  !updatingAI && (

  <button
    type="button"
    className="secondary-button"
    disabled={
      reviewing ||
      savingEdit ||
      updatingWithAI ||
      historyLoading
    }
    onClick={() => {

      setHistoryVersion(
        null
      );

      setShowHistory(
        (current) =>
          !current
      );
    }}
  >
    {historyLoading
      ? "Loading History..."
      : showHistory
        ? "Hide Version History"
        : "Version History"}
  </button>

)}

          {isDraft &&
  !isLegacy &&
  !editing &&
  !updatingAI &&
  !showHistory && (

  <>

    <button
      type="button"
      className="reject-button"
      disabled={
        reviewing ||
        updatingWithAI
      }
      onClick={onReject}
    >
      {reviewing
        ? "Updating..."
        : "Reject Automation"}
    </button>


    <button
      type="button"
      className="approve-button"
      disabled={
        reviewing ||
        updatingWithAI
      }
      onClick={onApprove}
    >
      {reviewing
        ? "Updating..."
        : "Approve for Execution"}
    </button>

  </>

)}


          {!editing &&
  !updatingAI && (

  <button
    type="button"
    className="secondary-button"
    disabled={
      reviewing ||
      savingEdit ||
      updatingWithAI
    }
    onClick={onClose}
  >
    Close
  </button>

)}

        </div>

      </div>

    </div>
  );
}


export default AutomationViewerModal;