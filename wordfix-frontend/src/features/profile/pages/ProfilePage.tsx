import PageTransition from '@/components/shared/PageTransition';
import ProfileHeader from '../components/ProfileHeader';
import ProfileInfoCard from '../components/ProfileInfoCard';
import ChangePasswordCard from '../components/ChangePasswordCard';
import LearningLevelCard from '../components/LearningLevelCard';

export function ProfilePage() {
  return (
    <PageTransition>
      <div className="max-w-2xl mx-auto space-y-6">
        <ProfileHeader />
        <ProfileInfoCard />
        <ChangePasswordCard />
        <LearningLevelCard />
      </div>
    </PageTransition>
  );
}

export default ProfilePage;

