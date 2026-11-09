import MetricCard from "../components/MetricCard";


function ProjectWorkspacePage({
  project,
  requirements,
  testCases,
  scenarios,
  loading,
  scenariosLoading,
  analysingRequirementId,
  generatingScenariosRequirementId,
  getRequirementTestCount,
  getRequirementScenarioCount,
  getRequirementAIScenarioCount,
  onBack,
  onViewTestCases,
  onAddRequirement,
  onAnalyseRequirement,
  onGenerateScenarios,
  onViewScenarios,
}) {
  return (
    <section className="workspace-page">

      <div className="workspace-header">

        <div>

          <button
            type="button"
            className="back-button"
            onClick={onBack}
          >
            ← Back to Projects
          </button>

          <span className="section-label">
            PROJECT WORKSPACE
          </span>

          <h3>
            {project.name}
          </h3>

          <p>
            {project.description}
          </p>

          <div className="workspace-tags">

            <span>
              {project.application_type
                .toUpperCase()}
            </span>

            <span>
              Project #{project.id}
            </span>

          </div>

        </div>


        <div className="workspace-header-actions">

          <button
            type="button"
            className="secondary-button"
            disabled={
              testCases.length === 0
            }
            onClick={onViewTestCases}
          >
            View Test Cases
          </button>

          <button
            type="button"
            className="primary-button"
            onClick={onAddRequirement}
          >
            + Add Requirement
          </button>

        </div>

      </div>


      <div className="workspace-summary">

        <MetricCard
          label="Requirements"
          value={
            requirements.length
          }
          detail="Captured in this project"
        />

        <MetricCard
          label="Scenarios"
          value={
            scenariosLoading
              ? "..."
              : scenarios.length
          }
          detail="Mapped to requirements"
        />

        <MetricCard
          label="Test Cases"
          value={
            testCases.length
          }
          detail="Generated and persisted"
        />

        <MetricCard
          label="Application"
          value={
            project.application_type
              .toUpperCase()
          }
          detail="Testing mode"
        />

      </div>


      <div className="workspace-section">

        <div className="panel-header">

          <div>

            <span className="section-label">
              REQUIREMENTS
            </span>

            <h3>
              Project Requirements
            </h3>

          </div>

        </div>


        {loading ? (

          <div className="api-status">
            Loading project requirements...
          </div>

        ) : requirements.length === 0 ? (

          <div className="empty-state">

            <h4>
              No requirements yet
            </h4>

            <p>
              Add your first software
              requirement to begin QA
              analysis.
            </p>

          </div>

        ) : (

          <div className="requirement-list">

            {requirements.map(
              (requirement) => {

                const testCount =
                  getRequirementTestCount(
                    requirement.id
                  );

                const scenarioCount =
                  getRequirementScenarioCount(
                    requirement.id
                  );

                const aiScenarioCount =
                  getRequirementAIScenarioCount(
                    requirement.id
                  );


                return (
                  <article
                    className="requirement-card"
                    key={requirement.id}
                  >

                    <div className="requirement-main">

                      <div className="requirement-heading">

                        <span className="requirement-id">
                          {
                            requirement
                              .requirement_id
                          }
                        </span>

                        <span className="requirement-type">
                          {
                            requirement
                              .application_type
                              .toUpperCase()
                          }
                        </span>

                      </div>


                      <h4>
                        {requirement.title}
                      </h4>

                      <p>
                        {requirement.description}
                      </p>


                      <div className="requirement-counts">

                        <span>
                          {scenariosLoading
                            ? "..."
                            : scenarioCount}
                          {" "}
                          {scenarioCount === 1
                            ? "Scenario"
                            : "Scenarios"}
                        </span>

                        <span>
                          {testCount}
                          {" "}
                          {testCount === 1
                            ? "Test Case"
                            : "Test Cases"}
                        </span>

                      </div>

                    </div>


                    <div className="requirement-actions">

                      <button
                        type="button"
                        className="secondary-button"
                        disabled={
                          analysingRequirementId ===
                          requirement.id
                        }
                        onClick={() =>
                          onAnalyseRequirement(
                            requirement
                          )
                        }
                      >
                        {analysingRequirementId ===
                        requirement.id
                          ? "Analysing..."
                          : "Analyse"}
                      </button>


                      <button
                        type="button"
                        className="primary-button"
                        disabled={
                          generatingScenariosRequirementId ===
                            requirement.id ||
                          aiScenarioCount > 0
                        }
                        onClick={() =>
                          onGenerateScenarios(
                            requirement
                          )
                        }
                      >
                        {generatingScenariosRequirementId ===
                        requirement.id
                          ? "Generating Scenarios..."
                          : aiScenarioCount > 0
                            ? "AI Scenarios Generated"
                            : "Generate AI Scenarios"}
                      </button>


                      <button
                        type="button"
                        className="secondary-button"
                        disabled={
                          scenariosLoading
                        }
                        onClick={() =>
                          onViewScenarios(
                            requirement
                          )
                        }
                      >
                        {scenariosLoading
                          ? "Loading..."
                          : "View Scenarios"}
                      </button>

                    </div>

                  </article>
                );
              }
            )}

          </div>

        )}

      </div>

    </section>
  );
}


export default ProjectWorkspacePage;