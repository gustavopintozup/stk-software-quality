from templateframework.metadata import Metadata
import os

def run(metadata: Metadata = None):
    
    target_project = str(metadata.target_path)
    output_file = "output.json"

    def clean_temp_files():
        from os.path import exists

        if exists(output_file):
            os.remove(output_file)

    def find_sorald_jar():
        import glob
        home = os.path.expanduser('~')

        for file in glob.glob(home + "/.stk/stacks/*/stk-sonarqube-repair-plugin/sorald.jar"):
            return os.path.abspath(file)

    def run_java_cmd(parametros):
        sorald_dir = find_sorald_jar()

        java_cmd = ["java", "-jar", sorald_dir]
        java_cmd.extend(parametros)

        import subprocess
        result = subprocess.run(java_cmd,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
        return result

    print("Searching for SonarQube violations..")

    violated_rules = ["mine", "--source", target_project,
                            "--handled-rules", "--stats-output-file", output_file]

    result = run_java_cmd(violated_rules)

    if result.stderr == "":
        import json
        with open(output_file) as mining_output:
            json_output = json.load(mining_output)
            violations_found = json_output["minedRules"]

            import questionary

            print("We found a total of %s violations" % len(violations_found))
            vai_reparar = questionary.select(
                "Do you want to repair any violation?",
                choices=["Yes", "No"],
            ).ask()

            if vai_reparar == "Yes":
                list_of_violations = [v['ruleKey'] + ": " + v['ruleName'] for v in violations_found]
                violations_to_repair = questionary.checkbox("Check a violation", choices=list_of_violations).ask()

                for violation in violations_to_repair:
                    violation = violation.split(": ")[0]
                    repair_instruction = ["repair", "--source", target_project, "--rule-key", violation]

                    print("Repairing violation %s" % violation)
                    run_java_cmd(repair_instruction)

        clean_temp_files()
    else:
        for item in result.stderr.split("\n"):
           print(item)
            
    return metadata