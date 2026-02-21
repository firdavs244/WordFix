import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import ImportStepIndicator from './ImportStepIndicator';
import TextInputStep from './TextInputStep';
import TextAnalyzeButton from './TextAnalyzeButton';
import TextImportReview from './TextImportReview';
import TextImportResult from './TextImportResult';
import { useTextImport } from '../hooks/useTextImport';

export default function TextImportFlow() {
  const [step, setStep] = useState(0);
  const ti = useTextImport();

  const handleAnalyze = async () => {
    await ti.analyze();
    setStep(1);
  };

  const handleImport = async () => {
    await ti.importSelected();
    setStep(2);
  };

  return (
    <div>
      <ImportStepIndicator currentStep={step} steps={['Input', 'Review', 'Done']} />
      <div className="mt-6">
        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div key="input" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <TextInputStep text={ti.text} onChange={ti.setText} />
              <div className="mt-4 flex justify-end">
                <TextAnalyzeButton onClick={handleAnalyze} isLoading={ti.isAnalyzing} disabled={!ti.text.trim()} />
              </div>
            </motion.div>
          )}
          {step === 1 && (
            <motion.div key="review" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <TextImportReview words={ti.suggestions} selectedIds={ti.selectedIds} onToggle={ti.toggle} onSelectAll={ti.selectAll} onDeselectAll={ti.deselectAll} onImport={handleImport} isImporting={ti.isImporting} />
            </motion.div>
          )}
          {step === 2 && (
            <motion.div key="result" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <TextImportResult importedCount={ti.importedCount} onImportMore={() => { ti.reset(); setStep(0); }} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
