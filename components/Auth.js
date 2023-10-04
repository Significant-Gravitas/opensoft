import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { Auth } from '@supabase/auth-ui-react';
import supabase from '../lib/supabaseClient';

function AuthComponent() {
  const router = useRouter();

  useEffect(() => {
    console.log('Setting up auth listener...');

    // Subscribe to authentication state changes
    const { data: authListener } = supabase.auth.onAuthStateChange(
      (event, session) => {
        console.log('Auth event:', event);
        if (
          event === 'SIGNED_IN' ||
          event === 'USER_UPDATED'
        ) {
          console.log('Attempting redirect...');
          router.push('/dashboard');
        }
      },
    );

    // Check if the user is already authenticated on component mount
    const user = supabase.auth.user;
    if (user) {
      console.log('User is authenticated, redirecting...');
      router.push('/dashboard');
    }

    // Cleanup the listener on component unmount
    return () => {
      console.log('Cleaning up auth listener...');
      if (authListener && typeof authListener.unsubscribe === 'function') {
        authListener.unsubscribe();
      }
    };
  }, [router]);

  console.log('Rendering AuthComponent');
  return <Auth supabaseClient={supabase} providers={['google']} />;
}

export default AuthComponent;
