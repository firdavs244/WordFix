import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Pencil } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuthStore } from '@/stores/useAuthStore';
import ProfileEditForm from './ProfileEditForm';

export default function ProfileInfoCard() {
  const user = useAuthStore((s) => s.user);
  const [editing, setEditing] = useState(false);

  if (!user) return null;

  const fields = [
    { label: 'Full Name', value: user.full_name || '—' },
    { label: 'Email', value: user.email },
    { label: 'Username', value: user.username },
    { label: 'Daily Goal', value: `${user.daily_goal} words/day` },
    { label: 'Proficiency', value: user.proficiency_level },
    { label: 'Timezone', value: user.timezone || 'UTC' },
  ];

  return (
    <div className="rounded-2xl shadow-card border border-border/50 p-6 bg-card">
      <div className="flex justify-between items-center">
        <h3 className="text-base font-heading font-semibold">Personal Information</h3>
        <Button variant="ghost" size="sm" className="text-xs text-primary gap-1" onClick={() => setEditing(!editing)}>
          <Pencil className="h-3.5 w-3.5" />
          {editing ? 'View' : 'Edit'}
        </Button>
      </div>
      <AnimatePresence mode="wait">
        {editing ? (
          <motion.div key="edit" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <ProfileEditForm onCancel={() => setEditing(false)} />
          </motion.div>
        ) : (
          <motion.div key="view" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4"
          >
            {fields.map((f) => (
              <div key={f.label}>
                <p className="text-[10px] uppercase tracking-wide text-muted-foreground/60 font-medium">{f.label}</p>
                <p className="text-sm font-medium mt-0.5">{f.value}</p>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
