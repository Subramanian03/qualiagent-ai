function AutomationPage({
  project,
  testCases = [],
  automationByTestCase = {},
  loadingAutomationId,
  preparingAutomationId,
  onPrepareAutomation,
  onViewAutomation,
  onRunTest,
  onBack
}) {
  if (!project) {
    return (
      <section className="automation-page">

        <div className="empty-state">

          <h4>
            No project selected
          </h4>

          <p>
            Open a project before using
            the Automation Workspace.
          </p>

        </div>

      </section>
    );
  }


  const safeTestCases =
    Array.isArray(testCases)
      ? testCases
      : [];


  /*
 * Automation Workspace eligibility
 * is controlled by the human QA
 * execution decision.
 *
 * AI automation_candidate remains
 * advisory only.
 */
const approvedAutomationTests =
  safeTestCases.filter(
    (testCase) => {

      const executionType =
        (
          testCase.execution_type ||
          "manual"
        ).toLowerCase();


      return (
        testCase.review_status ===
          "approved" &&
        (
          executionType ===
            "automation" ||
          executionType ===
            "both"
        )
      );
    }
  );


  return (
    <section className="automation-page">

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
            AUTOMATION
          </span>


          <h3>
            Automation Workspace
          </h3>


          <p>
  Approved Test Cases classified
  by QA as Automation or Both
  for {project.name}.
</p>


          <div className="workspace-tags">

            <span>
              {(project.application_type ||
                "unknown")
                .toUpperCase()}
            </span>

            <span>
              {approvedAutomationTests.length}
              {" "}
              Eligible
            </span>

          </div>

        </div>

      </div>


      <div className="automation-summary">

        <AutomationMetric
          label="Total Test Cases"
          value={
            safeTestCases.length
          }
        />


        <AutomationMetric
          label="Approved"
          value={
            safeTestCases.filter(
              (testCase) =>
                testCase.review_status ===
                "approved"
            ).length
          }
        />


        <AutomationMetric
          label="Eligible"
          value={
            approvedAutomationTests.length
          }
        />


        <AutomationMetric
          label="Draft Automation"
          value={
            approvedAutomationTests.filter(
              (testCase) => {

                const automation =
                  automationByTestCase[
                    testCase.id
                  ];

                return (
                  automation?.status ===
                    "draft" &&
                  Boolean(
                    automation.code?.trim()
                  )
                );
              }
            ).length
          }
        />


        <AutomationMetric
          label="Ready"
          value={
            approvedAutomationTests.filter(
              (testCase) => {

                const automation =
                  automationByTestCase[
                    testCase.id
                  ];

                return (
                  automation?.status ===
                    "ready" &&
                  Boolean(
                    automation.code?.trim()
                  )
                );
              }
            ).length
          }
        />

        <AutomationMetric
  label="Rejected"
  value={
    approvedAutomationTests.filter(
      (testCase) => {

        const automation =
          automationByTestCase[
            testCase.id
          ];

        return (
          automation?.status ===
          "rejected"
        );
      }
    ).length
  }
/>

      </div>


      <div className="automation-content">

        <div className="panel-header">

          <div>

            <span className="section-label">
              ELIGIBLE TESTS
            </span>

            <h3>
              Automation Pipeline
            </h3>

          </div>

        </div>


        {approvedAutomationTests.length ===
        0 ? (

          <div className="empty-state">

            <h4>
  No Test Cases classified for automation
</h4>

            <p>
  Approve a Test Case and set its
  Human Execution Decision to
  Automation or Both before preparing
  automation.
</p>

          </div>

        ) : (

          <div className="automation-test-list">

            {approvedAutomationTests.map(
              (testCase) => {

              const automation =
                automationByTestCase[
                  testCase.id
                ];


              const automationReady =
                automation?.status ===
                  "ready" &&
                Boolean(
                  automation.code?.trim()
                );


              const automationDraft =
                automation?.status ===
                  "draft" &&
                Boolean(
                  automation.code?.trim()
                );

              const automationRejected =
                   automation?.status ===
                     "rejected";


              const isBusy =
  loadingAutomationId ===
    testCase.id ||
  preparingAutomationId ===
    testCase.id;


              return (
                <article
                  className="automation-test-card"
                  key={testCase.id}
                >

                  <div>

                    <div className="generated-test-heading">

                      <span className="requirement-id">
                        {testCase.test_case_id}
                      </span>


                      <span className="review-status review-approved">
                        APPROVED
                      </span>


                      <span
  className={
    automationReady
      ? (
        "automation-state "
        + "automation-state-ready"
      )
      : automationDraft
        ? (
          "automation-state "
          + "automation-state-draft"
        )
        : automationRejected
          ? (
            "automation-state "
            + "automation-state-rejected"
          )
          : (
            "automation-state "
            + "automation-state-none"
          )
  }
>
  {automationReady
    ? "AUTOMATION READY"
    : automationDraft
      ? "AUTOMATION DRAFT"
      : automationRejected
        ? "AUTOMATION REJECTED"
        : "NOT GENERATED"}
</span>


                      <span className="requirement-type">
                        {(testCase.test_type ||
                          "unknown")
                          .toUpperCase()}
                      </span>

                    </div>


                    <h4>
                      {testCase.title}
                    </h4>


                    <p>
                      {testCase.requirement_id}
                    </p>


                    <div className="automation-card-meta">

                      <span>
  AI:
  {" "}
  {testCase.automation_candidate
    ? "Automation Candidate"
    : "Manual Candidate"}
</span>

                      <span>
  Human:
  {" "}
  {(
    testCase.execution_type ||
    "manual"
  ).toUpperCase()}
</span>


                      {automationDraft && (

                        <span>
                          Human Review Required
                        </span>

                      )}


                      {automationReady && (

                        <span>
                          Approved for Execution
                        </span>

                      )}

                      {automationRejected && (

  <span>
    Human Review Rejected
  </span>

)}

                    </div>

                  </div>


                  <div className="automation-card-actions">

  {automationReady ? (

    <>

      <button
        type="button"
        className="secondary-button"
        disabled={isBusy}
        onClick={() =>
          onViewAutomation(
            testCase
          )
        }
      >
        View Automation
      </button>


      <button
        type="button"
        className="primary-button"
        disabled={isBusy}
        onClick={() =>
          onRunTest(
            testCase
          )
        }
      >
        Run Test
      </button>

    </>

  ) : automationDraft ? (

    <button
      type="button"
      className="primary-button"
      disabled={isBusy}
      onClick={() =>
        onViewAutomation(
          testCase
        )
      }
    >
      Review Automation
    </button>

  ) : automationRejected ? (

    <button
      type="button"
      className="secondary-button"
      disabled={isBusy}
      onClick={() =>
        onViewAutomation(
          testCase
        )
      }
    >
      View Rejected Automation
    </button>

  ) : (

    <button
      type="button"
      className="primary-button"
      disabled={
        preparingAutomationId ===
        testCase.id
      }
      onClick={() =>
        onPrepareAutomation(
          testCase
        )
      }
    >
      {preparingAutomationId ===
      testCase.id
        ? "Preparing..."
        : "Prepare Automation"}
    </button>

  )}

</div>

                </article>
              );

            })}

          </div>

        )}

      </div>

    </section>
  );
}


function AutomationMetric({
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


export default AutomationPage;