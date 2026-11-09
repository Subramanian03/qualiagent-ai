import TestSummaryItem from
  "../components/testcases/TestSummaryItem";


function TestCasesPage({
  project,
  requirements,
  testCases,
  loading,
  updatingTestCaseId,
  onBack,
  onOpenTestCase
}) {
  if (!project) {
    return (
      <section className="test-case-page">

        <div className="empty-state">

          <h4>
            No project selected
          </h4>

          <p>
            Select a project before viewing
            its test cases.
          </p>

        </div>

      </section>
    );
  }


  function getRequirementTitle(
    requirementDbId
  ) {
    const requirement =
      requirements.find(
        (item) =>
          item.id === requirementDbId
      );

    return requirement
      ? requirement.title
      : "Unknown requirement";
  }


  const draftCount =
    testCases.filter(
      (testCase) =>
        testCase.review_status ===
        "draft"
    ).length;

  const approvedCount =
    testCases.filter(
      (testCase) =>
        testCase.review_status ===
        "approved"
    ).length;

  const rejectedCount =
    testCases.filter(
      (testCase) =>
        testCase.review_status ===
        "rejected"
    ).length;


  return (
    <section className="test-case-page">

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
            TEST DESIGN
          </span>

          <h3>
            Test Case Workspace
          </h3>

          <p>
            Review the generated and persisted
            test cases for {project.name}.
          </p>

          <div className="workspace-tags">

            <span>
              {project.application_type
                .toUpperCase()}
            </span>

            <span>
              {requirements.length}
              {" "}
              Requirements
            </span>

            <span>
              {testCases.length}
              {" "}
              Test Cases
            </span>

          </div>

        </div>

      </div>


      {loading ? (

        <div className="api-status">
          Loading test cases...
        </div>

      ) : testCases.length === 0 ? (

        <div className="empty-state">

          <h4>
            No test cases available
          </h4>

          <p>
            Return to the project workspace
            and generate test cases for a
            requirement.
          </p>

        </div>

      ) : (

        <div className="test-case-layout">

          <aside className="test-case-filters">

            <span className="section-label">
              SUMMARY
            </span>

            <TestSummaryItem
              label="Total"
              value={testCases.length}
            />

            <TestSummaryItem
              label="Draft"
              value={draftCount}
            />

            <TestSummaryItem
              label="Approved"
              value={approvedCount}
            />

            <TestSummaryItem
              label="Rejected"
              value={rejectedCount}
            />

            <TestSummaryItem
              label="Positive"
              value={
                testCases.filter(
                  (testCase) =>
                    testCase.test_type ===
                    "positive"
                ).length
              }
            />

            <TestSummaryItem
              label="Negative"
              value={
                testCases.filter(
                  (testCase) =>
                    testCase.test_type ===
                    "negative"
                ).length
              }
            />

            <TestSummaryItem
              label="Automation Candidates"
              value={
                testCases.filter(
                  (testCase) =>
                    testCase
                      .automation_candidate
                ).length
              }
            />

          </aside>


          <div className="test-case-list">

            {testCases.map(
              (testCase) => (

              <article
                className="test-case-view-card"
                key={testCase.id}
              >

                <div className="test-case-card-top">

                  <div className="generated-test-heading">

                    <span className="requirement-id">
                      {testCase.test_case_id}
                    </span>

                    <span className="requirement-type">
                      {testCase.test_type
                        .toUpperCase()}
                    </span>

                    <span className="priority-badge">
                      {testCase.priority
                        .toUpperCase()}
                    </span>

                    <span
                      className={
                        `review-status review-${
                          testCase.review_status ||
                          "draft"
                        }`
                      }
                    >
                      {(testCase.review_status ||
                        "draft")
                        .toUpperCase()}
                    </span>

                  </div>


                  <button
                    type="button"
                    className="text-button"
                    disabled={
                      updatingTestCaseId ===
                      testCase.id
                    }
                    onClick={() =>
                      onOpenTestCase(
                        testCase
                      )
                    }
                  >
                    {updatingTestCaseId ===
                    testCase.id
                      ? "Updating..."
                      : "View Details"}
                  </button>

                </div>


                <h4>
                  {testCase.title}
                </h4>

                <p className="test-case-requirement">

                  {testCase.requirement_id}

                  {" · "}

                  {getRequirementTitle(
                    testCase
                      .requirement_db_id
                  )}

                </p>


                <div className="generated-test-meta">

                  <span>
                    {testCase.steps.length}
                    {" "}
                    Steps
                  </span>

                  <span>
                    {testCase
                      .preconditions
                      .length}
                    {" "}
                    Preconditions
                  </span>

                  <span>
                    {testCase
                      .automation_candidate
                      ? "Automation Candidate"
                      : "Manual Candidate"}
                  </span>

                </div>

              </article>

            ))}

          </div>

        </div>

      )}

    </section>
  );
}


export default TestCasesPage;