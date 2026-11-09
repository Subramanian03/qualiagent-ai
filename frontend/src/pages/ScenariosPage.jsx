function ScenariosPage({
  project,
  requirement,
  scenarios = [],
  scenarioTestCases = {},
  loading,
  generatingScenarioTestCasesId,
  onGenerateTestCases,
  onBack,
  onOpenTestCase
}) {
  if (!project || !requirement) {
    return (
      <section className="scenarios-page">

        <div className="empty-state">
          <h4>
            Requirement unavailable
          </h4>

          <p>
            Open a requirement before viewing
            its test scenarios.
          </p>
        </div>

      </section>
    );
  }


  const requirementScenarios =
    scenarios.filter(
      (scenario) =>
        scenario.requirement_db_id ===
        requirement.id
    );


  const totalTests =
    requirementScenarios.reduce(
      (total, scenario) => {
        const tests =
          scenarioTestCases[
            scenario.id
          ];

        return (
          total +
          (
            Array.isArray(tests)
              ? tests.length
              : 0
          )
        );
      },
      0
    );


  return (
    <section className="scenarios-page">

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
            TEST SCENARIOS
          </span>

          <h3>
            {requirement.title}
          </h3>

          <p>
            {requirement.description}
          </p>

          <div className="workspace-tags">

            <span>
              {requirement.requirement_id}
            </span>

            <span>
              {requirement.application_type
                ?.toUpperCase() ||
                "UNKNOWN"}
            </span>

          </div>

        </div>

      </div>


      <div className="scenario-summary">

        <ScenarioMetric
          label="Scenarios"
          value={
            requirementScenarios.length
          }
        />

        <ScenarioMetric
          label="Test Cases"
          value={totalTests}
        />

        <ScenarioMetric
          label="Project"
          value={project.name}
        />

      </div>


      <div className="scenario-content">

        <div className="panel-header">

          <div>

            <span className="section-label">
              TRACEABILITY
            </span>

            <h3>
              Requirement → Scenarios → Test Cases
            </h3>

          </div>

        </div>


        {loading ? (

          <div className="api-status">
            Loading test scenarios...
          </div>

        ) : requirementScenarios.length ===
        0 ? (

          <div className="empty-state">

            <h4>
              No test scenarios yet
            </h4>

            <p>
              Test scenarios have not yet
              been generated for this
              requirement.
            </p>

          </div>

        ) : (

          <div className="scenario-list">

            {requirementScenarios.map(
              (scenario) => {

              const tests =
                Array.isArray(
                  scenarioTestCases[
                    scenario.id
                  ]
                )
                  ? scenarioTestCases[
                      scenario.id
                    ]
                  : [];

              const hasTestCases = tests.length > 0;

              const isGenerating = generatingScenarioTestCasesId === scenario.id;


              return (
                <article
                  className="scenario-card"
                  key={scenario.id}
                >

                  <div className="scenario-card-header">

                    <div>

                      <div className="scenario-heading">

                        <span className="requirement-id">
                          {scenario.scenario_id}
                        </span>

                        <span className="requirement-type">
                          {(scenario.scenario_type ||
                            "functional")
                            .toUpperCase()}
                        </span>

                        <span className="priority-badge">
                          {(scenario.priority ||
                            "medium")
                            .toUpperCase()}
                        </span>

                        <span
                          className={
                            `scenario-source scenario-source-${
                              scenario.source ||
                              "manual"
                            }`
                          }
                        >
                          {(scenario.source ||
                            "manual")
                            .toUpperCase()}
                        </span>

                      </div>


                      <h4>
                        {scenario.title}
                      </h4>


                      {scenario.description && (

                        <p>
                          {scenario.description}
                        </p>

                      )}

                    </div>


                    <div className="scenario-card-tools">

  <span className="scenario-test-count">
    {tests.length}
    {" "}
    {tests.length === 1
      ? "Test Case"
      : "Test Cases"}
  </span>


  {scenario.source !== "legacy" && (

  <button
    type="button"
    className="primary-button"
    disabled={
      isGenerating ||
      hasTestCases
    }
    onClick={() =>
      onGenerateTestCases(
        scenario
      )
    }
  >
    {isGenerating
      ? "Generating Test Cases..."
      : tests.length > 0
        ? "AI Test Cases Generated"
        : "Generate AI Test Cases"}
  </button>

)}

</div>

                  </div>


                  {tests.length === 0 ? (

                    <div className="scenario-tests-empty">
                      No test cases linked to
                      this scenario.
                    </div>

                  ) : (

                    <div className="scenario-test-list">

                      {tests.map(
                        (testCase) => (

                        <article
                          className="scenario-test-card"
                          key={testCase.id}
                        >

                          <div>

                            <div className="scenario-test-heading">

                              <span className="requirement-id">
                                {testCase.test_case_id}
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

                              <span className="requirement-type">
                                {(testCase.test_type ||
                                  "functional")
                                  .toUpperCase()}
                              </span>

                            </div>


                            <h5>
                              {testCase.title}
                            </h5>


                            <p>
                              {(testCase.steps || [])
                                .length}
                              {" "}
                              Steps
                              {" · "}
                              {testCase.automation_candidate
                                ? "Automation Candidate"
                                : "Manual Candidate"}
                            </p>

                          </div>


                          <button
                            type="button"
                            className="secondary-button"
                            onClick={() =>
                              onOpenTestCase(
                                testCase
                              )
                            }
                          >
                            View Details
                          </button>

                        </article>

                      ))}

                    </div>

                  )}

                </article>
              );

            })}

          </div>

        )}

      </div>

    </section>
  );
}


function ScenarioMetric({
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


export default ScenariosPage;