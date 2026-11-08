/* Discrete Math Unit 2 cheat sheet (The Logic of Compound Statements). Truth columns are recomputed by the checks. */
const col = (f, n) => { const out = []; for (let m = 0; m < (1 << n); m++) { const v = []; for (let k = 0; k < n; k++) v.push(!((m >> (n - 1 - k)) & 1)); out.push(f(...v) ? 'T' : 'F'); } return out.join(''); };
const imp = (a, b) => !a || b;
module.exports = {
  name: 'discrete-compound-statements-logic', course: 'Discrete Math', unitNo: 2, unitName: 'The Logic of Compound Statements',
  focus: 'connectives, truth tables, logical equivalence, conditionals and their negations',
  morefocus: 'converse, inverse and contrapositive; valid arguments, rules of inference and fallacies',
  front: [
    { title: 'Connectives', color: 'purple', kind: 'table', head: ['Symbol', 'Read', 'True when'], rows: [
      ['⟨\\neg p⟩', 'not ⟨p⟩', '⟨p⟩ is false'],
      ['⟨p \\wedge q⟩', '⟨p⟩ and ⟨q⟩', 'both true'],
      ['⟨p \\vee q⟩', '⟨p⟩ or ⟨q⟩ (inclusive)', 'at least one true'],
      ['⟨p \\oplus q⟩', 'exclusive or', 'exactly one true'],
      ['⟨p \\to q⟩', 'if ⟨p⟩ then ⟨q⟩', 'not (⟨p⟩ T and ⟨q⟩ F)'],
      ['⟨p \\leftrightarrow q⟩', '⟨p⟩ if and only if ⟨q⟩', 'same truth value']],
      after: 'Order of operations: ⟨\\neg⟩ first, then ⟨\\wedge⟩, then ⟨\\vee⟩, then ⟨\\to⟩, then ⟨\\leftrightarrow⟩. Use parentheses when unsure.' },
    { title: 'Truth Table Rows', color: 'blue', kind: 'table', head: ['⟨p⟩', '⟨q⟩', '⟨p \\wedge q⟩', '⟨p \\vee q⟩', '⟨p \\to q⟩', '⟨p \\leftrightarrow q⟩'], rows: [
      ['T', 'T', 'T', 'T', 'T', 'T'], ['T', 'F', 'F', 'T', '<b>F</b>', 'F'], ['F', 'T', 'F', 'T', 'T', 'F'], ['F', 'F', 'F', 'F', 'T', 'T']],
      after: 'Standard order: TT, TF, FT, FF. With ⟨n⟩ variables a table has ⟨2^n⟩ rows.',
      check: [{ true: `"${col((p, q) => p && q, 2)}" === "TFFF"` }, { true: `"${col((p, q) => p || q, 2)}" === "TTTF"` }, { true: `"${col((p, q) => imp(p, q), 2)}" === "TFTT"` }, { true: `"${col((p, q) => p === q, 2)}" === "TFFT"` }] },
    { title: 'Key Equivalences', color: 'green', kind: 'table', plain: true, head: ['Law', 'Equivalence'], rows: [
      ['De Morgan', '⟨\\neg(p \\wedge q) \\equiv \\neg p \\vee \\neg q⟩, ⟨\\neg(p \\vee q) \\equiv \\neg p \\wedge \\neg q⟩'],
      ['Conditional', '⟨p \\to q \\equiv \\neg p \\vee q⟩'],
      ['Contrapositive', '⟨p \\to q \\equiv \\neg q \\to \\neg p⟩'],
      ['Distributive', '⟨p \\wedge (q \\vee r) \\equiv (p \\wedge q) \\vee (p \\wedge r)⟩'],
      ['Absorption', '⟨p \\vee (p \\wedge q) \\equiv p⟩'],
      ['Biconditional', '⟨p \\leftrightarrow q \\equiv (p \\to q) \\wedge (q \\to p)⟩']],
      check: [{ true: `"${col((p, q) => !(p && q), 2)}" === "${col((p, q) => !p || !q, 2)}"` }, { true: `"${col((p, q) => imp(p, q), 2)}" === "${col((p, q) => imp(!q, !p), 2)}"` }, { true: `"${col((p, q, r) => p && (q || r), 3)}" === "${col((p, q, r) => (p && q) || (p && r), 3)}"` }] },
    { title: 'Showing Equivalence', color: 'orange', kind: 'example', text: 'Two forms are equivalent when their truth columns match in <b>every</b> row.',
      example: 'Is ⟨\\neg(p \\wedge q)⟩ equivalent to ⟨\\neg p \\wedge \\neg q⟩?', steps: [['Columns:', 'FTTT vs FFFT'], ['Row TF:', 'first is T, second is F']], answer: 'Not equivalent',
      check: [{ true: `"${col((p, q) => !(p && q), 2)}" === "FTTT"` }, { true: `"${col((p, q) => !p && !q, 2)}" === "FFFT"` }] },
    { title: 'Negating Conditionals', color: 'pink', kind: 'example', text: '⟨\\neg(p \\to q) \\equiv p \\wedge \\neg q⟩. The negation of an if-then statement is an <b>and</b> statement, not another if-then.',
      example: 'Negate: “If it is sunny, then we go to the beach.”', steps: [['Pattern:', '⟨p \\wedge \\neg q⟩'], ['Words:', 'It is sunny and we do not go to the beach.']], answer: 'sunny and no beach',
      check: { true: `"${col((p, q) => !imp(p, q), 2)}" === "${col((p, q) => p && !q, 2)}"` } },
    { title: 'Tautology or Contradiction', color: 'teal', kind: 'table', plain: true, head: ['Form', 'Type'], rows: [
      ['⟨p \\vee \\neg p⟩', 'tautology (always T)'], ['⟨p \\wedge \\neg p⟩', 'contradiction (always F)'], ['⟨(p \\wedge (p \\to q)) \\to q⟩', 'tautology'], ['⟨p \\to q⟩', 'neither (contingent)']],
      check: [{ true: `"${col(p => p || !p, 1)}" === "TT"` }, { true: `"${col((p, q) => imp(p && imp(p, q), q), 2)}" === "TTTT"` }] }
  ],
  back: [
    { title: 'Converse, Inverse, Contrapositive', color: 'purple', kind: 'table', head: ['Form', 'Symbols', 'Equivalent to ⟨p \\to q⟩?'], rows: [
      ['statement', '⟨p \\to q⟩', '—'], ['converse', '⟨q \\to p⟩', 'no'], ['inverse', '⟨\\neg p \\to \\neg q⟩', 'no (it matches the converse)'], ['contrapositive', '⟨\\neg q \\to \\neg p⟩', '<b>yes</b>']],
      after: 'Example ⟨p \\to q⟩: “If ⟨x = 2⟩, then ⟨x^2 = 4⟩” (true). Converse “If ⟨x^2 = 4⟩, then ⟨x = 2⟩” is false (⟨x = -2⟩).',
      check: [{ true: `"${col((p, q) => imp(q, p), 2)}" === "${col((p, q) => imp(!p, !q), 2)}"` }, { true: `"${col((p, q) => imp(p, q), 2)}" !== "${col((p, q) => imp(q, p), 2)}"` }] },
    { title: 'Valid Argument Forms', color: 'blue', kind: 'table', plain: true, head: ['Rule', 'Form'], rows: [
      ['modus ponens', '⟨p \\to q,\\ p\\ \\therefore\\ q⟩'],
      ['modus tollens', '⟨p \\to q,\\ \\neg q\\ \\therefore\\ \\neg p⟩'],
      ['transitivity', '⟨p \\to q,\\ q \\to r\\ \\therefore\\ p \\to r⟩'],
      ['elimination', '⟨p \\vee q,\\ \\neg p\\ \\therefore\\ q⟩'],
      ['division into cases', '⟨p \\vee q,\\ p \\to r,\\ q \\to r\\ \\therefore\\ r⟩'],
      ['contradiction rule', '⟨\\neg p \\to c\\ \\therefore\\ p⟩ (⟨c⟩ always false)']] },
    { title: 'Testing Validity', color: 'green', kind: 'example', text: 'An argument is <b>valid</b> if every row that makes all premises true also makes the conclusion true. One bad row makes it invalid.',
      example: '⟨p \\to q,\\ q\\ \\therefore\\ p⟩', steps: [['Find a bad row:', 'make ⟨p⟩ false, ⟨q⟩ true'], ['Check:', '⟨p \\to q⟩ T, ⟨q⟩ T, conclusion ⟨p⟩ F']], answer: 'Invalid (converse error)',
      check: { true: 'imp(false, true) && true && !false'.replace(/imp\(false, true\)/, '(!false || true)') } },
    { title: 'Fallacies', color: 'orange', kind: 'table', plain: true, head: ['Name', 'Invalid form and example'], rows: [
      ['converse error', '⟨p \\to q,\\ q\\ \\therefore\\ p⟩: “The grass is wet, so it rained.”'],
      ['inverse error', '⟨p \\to q,\\ \\neg p\\ \\therefore\\ \\neg q⟩: “It did not rain, so the grass is dry.”'],
      ['inclusive or', '⟨p \\vee q,\\ p\\ \\therefore\\ \\neg q⟩: both could be true']],
      after: 'An invalid argument can still have a true conclusion; validity is about the <b>form</b>.' },
    { title: 'Common Mistakes', color: 'pink', kind: 'mistakes',
      good: ['Check every row before calling forms equivalent.', 'Write the negation of ⟨p \\to q⟩ as ⟨p \\wedge \\neg q⟩.', 'Count rows: ⟨2^{(\\text{number of variables})}⟩.'],
      bad: [['Treating “or” as exclusive', '⟨\\vee⟩ is inclusive'], ['Calling the converse equivalent', 'only the contrapositive is'], ['De Morgan without switching ⟨\\wedge \\leftrightarrow \\vee⟩', 'switch the connective too']] },
    { title: 'Challenge: Knights and Knaves', color: 'teal', kind: 'html',
      html: 'Knights always tell the truth; knaves always lie. A says “B is a knave.” B says “A and I are the same type.”<br><b>Case A knight:</b> B is a knave, and B’s claim (“same type”) is false — consistent.<br><b>Case A knave:</b> B is a knight, but then B’s claim is false — impossible.<br><b>Answer:</b> A is a knight, B is a knave (division into cases plus the contradiction rule).' }
  ]
};
