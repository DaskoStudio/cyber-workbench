export default function Home() {
  return (
    <main>
      <p className="eyebrow">Portfolio · DaskoStudio</p>
      <h1>Cyber Workbench</h1>
      <p>Un socle pour explorer une architecture de cybersécurité full-stack.</p>
      <section aria-labelledby="scope">
        <h2 id="scope">Dépôt vitrine</h2>
        <p>Code de base / architecture ; fonctionnalités clés privées.</p>
        <ul><li>Interface Next.js</li><li>API FastAPI : santé et routes stubs</li><li>Runner Go : commandes stubs</li></ul>
        <p>Les outils renvoient « not implemented » et n’exécutent aucune opération réseau.</p>
      </section>
    </main>
  );
}
