from templateframework.metadata import Metadata
import os

def run(metadata: Metadata = None):
    
    target_project = str(metadata.target_path)
    output_file = "output.json"

    def limpar_arquivos_temporarios():
        from os.path import exists

        if exists(output_file):
            os.remove(output_file)

    def encontar_jar_sorald():
        import glob
        home = os.path.expanduser('~')

        for file in glob.glob(home + "/.stk/stacks/*/stk-sonarqube-repair-plugin/sorald.jar"):
            return os.path.abspath(file)

    def rodar_comando_java(parametros):
        sorald_dir = encontar_jar_sorald()

        comando_java = ["java", "-jar", sorald_dir]
        comando_java.extend(parametros)

        import subprocess
        result = subprocess.run(comando_java,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
        return result

    print("Searching for SonarQube violations..")

    instrucao_de_violacoes = ["mine", "--source", target_project,
                            "--handled-rules", "--stats-output-file", output_file]

    result = rodar_comando_java(instrucao_de_violacoes)

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
                lista_de_violacoes = [v['ruleKey'] + ": " + v['ruleName'] for v in violations_found]
                violacoes_para_reparar = questionary.checkbox("Check a violation", choices=lista_de_violacoes).ask()

                for violacao in violacoes_para_reparar:
                    violacao = violacao.split(": ")[0]
                    instrucao_de_reparo = ["repair", "--source", target_project, "--rule-key", violacao]

                    print("Repairing violation %s" % violacao)
                    rodar_comando_java(instrucao_de_reparo)

        limpar_arquivos_temporarios()
    else:
        for item in result.stderr.split("\n"):
           print(item)
            
    return metadata