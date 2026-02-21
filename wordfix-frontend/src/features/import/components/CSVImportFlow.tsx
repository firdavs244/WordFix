import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import ImportStepIndicator from './ImportStepIndicator';
import CSVDropZone from './CSVDropZone';
import CSVPreview from './CSVPreview';
import CSVResult from './CSVResult';
import { useCSVImport } from '../hooks/useCSVImport';

export default function CSVImportFlow() {
  const [step, setStep] = useState(0);
  const csv = useCSVImport();

  const handleFileSelect = async (file: File) => {
    await csv.validate(file);
    setStep(1);
  };

  const handleImport = async () => {
    await csv.importFile();
    setStep(2);
  };

  return (
    <div>
      <ImportStepIndicator currentStep={step} steps={['Upload', 'Preview', 'Done']} />
      <div className="mt-6">
        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div key="upload" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <CSVDropZone onFileSelect={handleFileSelect} selectedFile={csv.file} />
            </motion.div>
          )}
          {step === 1 && csv.previewData && (
            <motion.div key="preview" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <CSVPreview data={csv.previewData} onImport={handleImport} isImporting={csv.isImporting} />
            </motion.div>
          )}
          {step === 2 && csv.result && (
            <motion.div key="result" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <CSVResult result={csv.result} onImportMore={() => { csv.reset(); setStep(0); }} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
