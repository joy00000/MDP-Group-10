package com.example.mdp.adapter;

import android.content.Context;

import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;

import com.example.mdp.tabs.ChatFragment;
import com.example.mdp.Controller.ControllerFragment;
import com.example.mdp.tabs.ConfigurationFragment;
import com.example.mdp.R;
import com.example.mdp.tabs.PlaceholderFragment;

public class SectionsPagerAdapter extends FragmentPagerAdapter {
    @StringRes
    private static final int[] TABS = new int[]{R.string.tab_name1,R.string.tab_name2, R.string.tab_name3};

    private final Context pContext;


    public SectionsPagerAdapter(Context context, FragmentManager fm){
        super(fm);
        pContext = context;
    }

    @Override
    public Fragment getItem(int position){
        switch(position){
            case 0:
                return ConfigurationFragment.newInstance(position+1);
            case 1:
                return ControllerFragment.newInstance(position+1);
            case 2:
                return ChatFragment.newInstance(position+1);

            default:
                return PlaceholderFragment.newInstance(position + 1);
        }
    }

    @Nullable
    @Override
    public CharSequence getPageTitle(int pos){
        return pContext.getResources().getString(TABS[pos]);
    }

    @Override
    public int getCount(){
        return 3;
    }

}
